from typing import Any, Callable, List, TypedDict, Awaitable
from langchain.tools import StructuredTool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import create_tool_calling_agent, AgentExecutor
from .llm_utils import create_langchain_llm_from_env


class GraphState(TypedDict):
    input: str
    is_honorific: bool
    intent_pay_amount: bool
    tool_eligible: bool
    output: str


def make_node_politeness() -> Callable[[GraphState], Any]:
    async def node_politeness(state: GraphState) -> GraphState:
        llm = create_langchain_llm_from_env("NODE_POLITENESS")
        instruction = (
            "사용자 발화가 한국어 존대말(높임말)인지 판별하라. 반말이거나 애매하면 NO, 존대말이면 YES.\n"
            "반드시 YES 또는 NO만 출력하라. 다른 말 금지."
        )
        prompt_text = f"[Instruction]\n{instruction}\n\n[User Input]\n{state['input']}"
        resp = await llm.ainvoke(prompt_text)
        content = getattr(resp, "content", "").strip().upper()
        return {**state, "is_honorific": content.startswith("Y")}

    return node_politeness


def node_polite_warning(state: GraphState) -> GraphState:
    return {**state, "output": "존대말을 써주세요"}


def make_node_classify_pay_amount() -> Callable[[GraphState], Any]:
    async def node_classify_pay_amount(state: GraphState) -> GraphState:
        llm = create_langchain_llm_from_env("NODE_PAY_INTENT")
        instruction = (
            "다음 사용자 발화에 '금액을 지불(결제)하겠다는 의사'가 분명히 포함되어 있으면 YES,\n"
            "(숫자나 금액 표현 포함 등) 그렇지 않거나 정보가 부족하면 NO만 출력하라. 다른 말 금지."
        )
        prompt_text = f"[Instruction]\n{instruction}\n\n[User Input]\n{state['input']}"
        resp = await llm.ainvoke(prompt_text)
        content = getattr(resp, "content", "").strip().upper()
        return {**state, "intent_pay_amount": content.startswith("Y")}

    return node_classify_pay_amount


def node_ask_product(state: GraphState) -> GraphState:
    return {
        **state,
        "output": "어떤 상품을 구매하시나요? 구체적으로 알려주세요.",
    }


def make_node_check_tool(get_tools: Callable[[], Awaitable[List[StructuredTool]]]) -> Callable[[GraphState], Any]:
    async def node_check_tool(state: GraphState) -> GraphState:
        tools = await get_tools()
        tool_lines = []
        for tool in tools:
            name = getattr(tool, "name", "")
            desc = getattr(tool, "description", "")
            tool_lines.append(f"- {name}: {desc}")
        tools_text = "\n".join(tool_lines) if tool_lines else "(no tools)"

        llm = create_langchain_llm_from_env("NODE_TOOL_CHECK")
        instruction = (
            "너는 제공된 MCP 도구 목록을 보고, 사용자 요청이 '특정 상품 구매/주문/결제'를 실제 수행할 수 있는 도구가 있는지 판단한다.\n"
            "도구의 이름/설명 상 해당 액션을 수행할 수 있다고 합리적으로 볼 수 있을 때만 YES, 아니면 NO.\n"
            "반드시 대문자 YES 또는 NO만 출력하라. 추가 설명 금지."
        )
        prompt_text = (
            f"[Instruction]\n{instruction}\n\n"
            f"[User Input]\n{state['input']}\n\n"
            f"[Tools]\n{tools_text}\n"
        )
        try:
            resp = await llm.ainvoke(prompt_text)
            content = getattr(resp, "content", "").strip().upper()
            eligible = content.startswith("Y")
        except Exception:
            eligible = False
        return {**state, "tool_eligible": eligible}

    return node_check_tool


def make_node_agent(get_tools: Callable[[], Awaitable[List[StructuredTool]]]) -> Callable[[GraphState], Any]:
    async def node_agent(state: GraphState) -> GraphState:
        tools = await get_tools()
        llm = create_langchain_llm_from_env("NODE_AGENT")
        prompt = ChatPromptTemplate.from_messages([
            ("system", "너는 제공된 MCP 툴 중 적절한 것을 선택해 호출한다. 필요 없으면 직접 답하라."),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])
        agent = create_tool_calling_agent(llm, tools, prompt)
        executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)
        res = await executor.ainvoke({"input": state["input"]})
        out = res.get("output", "(출력 없음)")
        return {**state, "output": out}

    return node_agent


def node_no_tool(state: GraphState) -> GraphState:
    return {**state, "output": "적절한 tool 이 존재하지 않습니다."}


