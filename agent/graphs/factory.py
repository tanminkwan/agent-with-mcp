from __future__ import annotations

import os
from typing import Dict, Type

from .base import GraphInterface
from .purchase_graph import PurchaseFlowGraph


_REGISTRY: Dict[str, Type[GraphInterface]] = {
    "purchase": PurchaseFlowGraph,
    "purchase_flow": PurchaseFlowGraph,
}


def create_from_env() -> GraphInterface:
    """환경변수 AGENT_GRAPH로 그래프 구현을 선택하여 생성한다."""
    name = os.getenv("AGENT_GRAPH", "purchase").lower()
    return create(name)


def create(name: str) -> GraphInterface:
    key = name.lower()
    if key not in _REGISTRY:
        available = ", ".join(sorted(_REGISTRY.keys()))
        raise ValueError(f"알 수 없는 그래프: {name}. 사용 가능: {available}")
    return _REGISTRY[key]()


