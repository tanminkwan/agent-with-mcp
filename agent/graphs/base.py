from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict


class GraphInterface(ABC):
    """
    대화/흐름 그래프의 공통 인터페이스.
    다양한 그래프 구현이 이 인터페이스를 준수하여 교체/확장이 가능하도록 함.
    """

    @abstractmethod
    async def ainvoke(self, input_text: str) -> Dict[str, Any]:
        """비동기 실행. 상태 딕셔너리를 반환한다."""
        raise NotImplementedError

    def invoke(self, input_text: str) -> Dict[str, Any]:
        """동기 실행 헬퍼. 이벤트 루프가 없을 때만 사용."""
        import asyncio

        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = None

        if loop and loop.is_running():
            # 이미 실행 중인 루프가 있으면 비동기 사용을 강제
            raise RuntimeError("invoke()는 실행 중인 이벤트 루프 내에서 사용할 수 없습니다. ainvoke()를 사용하세요.")
        return asyncio.run(self.ainvoke(input_text))

    def save_png(self, path: str) -> None:
        """가능한 경우 그래프 구조를 PNG로 저장(옵션)."""
        # 기본 구현 없음. 구현체에서 선택적으로 제공.
        return None


