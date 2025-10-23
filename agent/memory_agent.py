import asyncio
from typing import Optional

from agent.graphs.base import GraphInterface


class MemoryAgent:
    """
    그래프 주도 실행 에이전트.
    - 그래프 구현은 의존성 주입으로 제공(확장 가능)
    - LLM 선택은 각 노드에서 .env와 LLMFactory를 통해 독립적으로 수행
    """

    def __init__(self, graph: GraphInterface):
        self.graph = graph

    def chat(self, user_input: str) -> str:
        final_state = self.graph.invoke(user_input)
        output = final_state.get("output", "")
        return output if isinstance(output, str) else str(output)