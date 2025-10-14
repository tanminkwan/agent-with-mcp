"""
Ollama LLM 구현
BaseLLM을 상속받아 Ollama 전용 기능 구현
"""
from langchain_community.chat_models import ChatOllama
from .base_llm import BaseLLM


class OllamaLLM(BaseLLM):
    """
    Ollama LLM 구현 클래스
    
    SOLID 원칙:
    - 단일 책임 원칙(SRP): Ollama LLM 호출만 담당
    - 개방/폐쇄 원칙(OCP): BaseLLM 확장으로 구현
    - 리스코프 치환 원칙(LSP): BaseLLM으로 완전히 치환 가능
    """
    
    def _initialize(self) -> None:
        """Ollama LLM 클라이언트 초기화"""
        self.llm = ChatOllama(
            model=self.model,
            **self.config
        )
    
    def __call__(self, *args, **kwargs):
        """
        Ollama LLM 호출
        LangChain 인터페이스 호환
        
        Returns:
            Ollama LLM 응답
        """
        return self.llm(*args, **kwargs) 