"""
LLM Factory 패턴 구현
SOLID 원칙 중 의존성 역전 원칙과 개방/폐쇄 원칙을 적용
"""
from typing import Dict, Type
from .base_llm import BaseLLM
from .ollama import OllamaLLM
from .openai_llm import OpenAILLM
from .vllm_llm import VLLMLLM


class LLMFactory:
    """
    LLM 인스턴스를 생성하는 팩토리 클래스
    
    SOLID 원칙:
    - 단일 책임 원칙(SRP): LLM 객체 생성만 담당
    - 개방/폐쇄 원칙(OCP): 새로운 LLM 추가 시 register 메서드로 확장
    - 의존성 역전 원칙(DIP): 구체 클래스가 아닌 BaseLLM 추상화를 반환
    
    Design Pattern: Factory Method Pattern
    """
    
    # LLM 제공자별 클래스 매핑
    _providers: Dict[str, Type[BaseLLM]] = {
        'ollama': OllamaLLM,
        'openai': OpenAILLM,
        'vllm': VLLMLLM,
    }
    
    @classmethod
    def create(cls, provider: str, model: str, **kwargs) -> BaseLLM:
        """
        LLM 인스턴스를 생성
        
        Args:
            provider: LLM 제공자 ('ollama', 'openai')
            model: 모델명
            **kwargs: 추가 설정 파라미터
            
        Returns:
            BaseLLM 인스턴스
            
        Raises:
            ValueError: 지원하지 않는 제공자인 경우
            
        Examples:
            >>> # Ollama 사용
            >>> llm = LLMFactory.create('ollama', 'llama2')
            
            >>> # OpenAI 사용
            >>> llm = LLMFactory.create('openai', 'gpt-4', temperature=0.7)
        """
        provider = provider.lower()
        
        if provider not in cls._providers:
            available = ', '.join(cls._providers.keys())
            raise ValueError(
                f"지원하지 않는 LLM 제공자입니다: {provider}\n"
                f"사용 가능한 제공자: {available}"
            )
        
        llm_class = cls._providers[provider]
        return llm_class(model=model, **kwargs)
    
    @classmethod
    def register(cls, provider: str, llm_class: Type[BaseLLM]) -> None:
        """
        새로운 LLM 제공자를 등록 (확장성 제공)
        
        Args:
            provider: LLM 제공자 이름
            llm_class: BaseLLM을 상속받은 클래스
            
        Raises:
            TypeError: BaseLLM을 상속받지 않은 클래스인 경우
            
        Examples:
            >>> class CustomLLM(BaseLLM):
            ...     pass
            >>> LLMFactory.register('custom', CustomLLM)
        """
        if not issubclass(llm_class, BaseLLM):
            raise TypeError(
                f"{llm_class.__name__}는 BaseLLM을 상속받아야 합니다."
            )
        
        cls._providers[provider.lower()] = llm_class
    
    @classmethod
    def get_available_providers(cls) -> list[str]:
        """사용 가능한 LLM 제공자 목록 반환"""
        return list(cls._providers.keys())

