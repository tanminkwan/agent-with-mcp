"""
OpenAI LLM 구현
BaseLLM을 상속받아 OpenAI 전용 기능 구현
"""
from langchain_openai import ChatOpenAI
from .base_llm import BaseLLM


class OpenAILLM(BaseLLM):
    """
    OpenAI LLM 구현 클래스
    
    SOLID 원칙:
    - 단일 책임 원칙(SRP): OpenAI LLM 호출만 담당
    - 개방/폐쇄 원칙(OCP): BaseLLM 확장으로 구현
    - 리스코프 치환 원칙(LSP): BaseLLM으로 완전히 치환 가능
    """
    
    def _initialize(self) -> None:
        """
        OpenAI LLM 클라이언트 초기화
        
        환경변수 OPENAI_API_KEY가 설정되어 있어야 함
        """
        # temperature, max_tokens 등의 추가 설정을 config에서 가져옴
        temperature = self.config.get('temperature', 0.7)
        max_tokens = self.config.get('max_tokens', None)
        
        self.llm = ChatOpenAI(
            model=self.model,
            temperature=temperature,
            max_tokens=max_tokens,
            **{k: v for k, v in self.config.items() 
               if k not in ['temperature', 'max_tokens']}
        )
    
    def __call__(self, *args, **kwargs):
        """
        OpenAI LLM 호출
        LangChain 인터페이스 호환
        
        Returns:
            OpenAI LLM 응답
        """
        return self.llm(*args, **kwargs)

