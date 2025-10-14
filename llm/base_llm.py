"""
LLM 추상 기반 클래스
SOLID 원칙 중 의존성 역전 원칙(DIP)을 적용하여 구체 클래스가 아닌 추상화에 의존하도록 함
"""
from abc import ABC, abstractmethod
from typing import Any


class BaseLLM(ABC):
    """
    모든 LLM 구현체가 상속받아야 하는 추상 기반 클래스
    
    SOLID 원칙:
    - 단일 책임 원칙(SRP): LLM 호출 인터페이스만 정의
    - 개방/폐쇄 원칙(OCP): 새로운 LLM 추가 시 이 클래스 수정 없이 확장 가능
    - 리스코프 치환 원칙(LSP): 모든 서브클래스는 이 클래스로 치환 가능
    """
    
    def __init__(self, model: str, **kwargs):
        """
        LLM 초기화
        
        Args:
            model: 사용할 모델명
            **kwargs: 추가 설정 파라미터
        """
        self.model = model
        self.config = kwargs
        self._initialize()
    
    @abstractmethod
    def _initialize(self) -> None:
        """
        LLM 클라이언트를 초기화하는 내부 메서드
        각 구현체에서 반드시 구현해야 함
        """
        pass
    
    @abstractmethod
    def __call__(self, *args, **kwargs) -> Any:
        """
        LLM을 호출하는 메서드
        LangChain 호환을 위해 __call__ 메서드로 구현
        
        Returns:
            LLM 응답 결과
        """
        pass
    
    def get_model_name(self) -> str:
        """모델명 반환"""
        return self.model
    
    def get_config(self) -> dict:
        """설정 정보 반환"""
        return self.config
    
    def as_langchain_model(self) -> Any:
        """
        내부 LangChain 모델을 반환
        LangChain의 ConversationChain 등과 호환되도록 함
        
        Returns:
            LangChain BaseChatModel 객체
        """
        if hasattr(self, 'llm'):
            return self.llm
        return self

