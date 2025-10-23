from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict, List

from dotenv import load_dotenv
from fastmcp import Client
from langchain.tools import StructuredTool
from langgraph.graph import StateGraph, START, END

from .base import GraphInterface
from agent.nodes.purchase_nodes import (
    GraphState,
    make_node_politeness,
    node_polite_warning,
    make_node_classify_pay_amount,
    node_ask_product,
    make_node_check_tool,
    make_node_agent,
    node_no_tool,
)


def _pyd_model_from_json_schema(name: str, schema: Dict[str, Any]):
    from pydantic import create_model

    schema = schema or {"type": "object", "properties": {}}
    props = schema.get("properties", {})
    req = set(schema.get("required", []))

    def pytype(t: str):
        return {
            "integer": int,
            "number": float,
            "boolean": bool,
            "object": dict,
            "array": list,
        }.get(t, str)

    fields = {k: (pytype(v.get("type", "string")), ... if k in req else None) for k, v in props.items()}
    return create_model(name, **fields) if fields else create_model(name)


def _make_langchain_tool_factory(config_path: str):
    """
    MCP tool 메타데이터를 읽어 LangChain StructuredTool 리스트를 생성하는 비동기 팩토리.
    노드 내부(이미 이벤트 루프가 실행 중)에서 안전하게 호출할 수 있도록 await 기반으로 동작한다.
    """

    async def get_tools() -> List[StructuredTool]:
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)

        async with Client(config) as client:
            mcp_tools = await client.list_tools()

        tools: List[StructuredTool] = []

        def _make_tool(name: str, desc: str, args_schema: Any) -> StructuredTool:
            async def _acall(**kwargs):
                async with Client(config) as _client:
                    res = await _client.call_tool(name, kwargs)
                    if hasattr(res, "content") and res.content:
                        texts = [c.text for c in res.content if hasattr(c, "text")]
                        return "\n".join(texts) if texts else str(res)
                    return str(res)

            return StructuredTool.from_function(
                name=name,
                description=desc,
                args_schema=args_schema,
                coroutine=_acall,
            )

        for t in mcp_tools:
            # Tool 객체 또는 dict 모두 호환
            name = getattr(t, "name", None) or (t.get("name") if isinstance(t, dict) else None)
            desc = getattr(t, "description", "") or (t.get("description") if isinstance(t, dict) else "")
            params = (
                getattr(t, "inputSchema", None)
                or getattr(t, "input_schema", None)
                or (t.get("inputSchema") if isinstance(t, dict) else None)
            )
            ArgsModel = _pyd_model_from_json_schema(f"{name}_Args", params)
            tools.append(_make_tool(name, desc, ArgsModel))

        return tools

    return get_tools


class PurchaseFlowGraph(GraphInterface):
    def __init__(self) -> None:
        load_dotenv()
        config_path = os.getenv(
            "MCP_SERVERS_CONFIG",
            str(Path(__file__).resolve().parents[2] / "mcp-server" / "mcp_servers.json"),
        )
        self._get_tools_async = _make_langchain_tool_factory(config_path)
        self._graph = self._build_graph()

    def _build_graph(self):
        workflow = StateGraph(GraphState)

        # 노드 팩토리들: 각 노드는 자체적으로 LLM을 선택
        workflow.add_node("politeness", make_node_politeness())
        workflow.add_node("polite_warning", node_polite_warning)
        workflow.add_node("classify_pay_amount", make_node_classify_pay_amount())
        workflow.add_node("ask_product", node_ask_product)
        workflow.add_node("check_tool", make_node_check_tool(self._get_tools_async))
        workflow.add_node("agent", make_node_agent(self._get_tools_async))
        workflow.add_node("no_tool", node_no_tool)

        # 엣지 구성
        workflow.add_edge(START, "politeness")

        def cond_polite(state: GraphState) -> bool:
            return state.get("is_honorific", False)

        workflow.add_conditional_edges(
            "politeness",
            cond_polite,
            {True: "classify_pay_amount", False: "polite_warning"},
        )

        def cond_pay_amount(state: GraphState) -> bool:
            return state.get("intent_pay_amount", False)

        workflow.add_conditional_edges(
            "classify_pay_amount",
            cond_pay_amount,
            {True: "check_tool", False: "ask_product"},
        )

        def cond_tool(state: GraphState) -> bool:
            return state.get("tool_eligible", False)

        workflow.add_conditional_edges(
            "check_tool",
            cond_tool,
            {True: "agent", False: "no_tool"},
        )

        workflow.add_edge("ask_product", END)
        workflow.add_edge("polite_warning", END)
        workflow.add_edge("agent", END)
        workflow.add_edge("no_tool", END)

        return workflow.compile()

    async def ainvoke(self, input_text: str) -> Dict[str, Any]:
        initial: GraphState = {
            "input": input_text,
            "is_honorific": False,
            "intent_pay_amount": False,
            "tool_eligible": False,
            "output": "",
        }
        return await self._graph.ainvoke(initial)

    def save_png(self, path: str) -> None:
        try:
            graph_representation = self._graph.get_graph()
            png_bytes = graph_representation.draw_mermaid_png()
            with open(path, "wb") as f:
                f.write(png_bytes)
        except Exception:
            # 선택적 기능: 실패해도 무시
            pass


