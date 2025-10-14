"""
LLM 모듈
다양한 LLM 제공자를 추상화하여 통합 인터페이스 제공

SOLID 원칙 적용:
- 단일 책임: 각 클래스는 하나의 LLM만 담당
- 개방/폐쇄: 새로운 LLM 추가 시 기존 코드 수정 없이 확장
- 리스코프 치환: 모든 구현체는 BaseLLM으로 치환 가능
- 인터페이스 분리: 클라이언트는 필요한 인터페이스만 사용
- 의존성 역전: 구체 클래스가 아닌 추상화에 의존

사용 예시:
    >>> from llm import LLMFactory
    >>> 
    >>> # Ollama 사용
    >>> llm = LLMFactory.create('ollama', 'llama2')
    >>> 
    >>> # OpenAI 사용
    >>> llm = LLMFactory.create('openai', 'gpt-4', temperature=0.7)
"""

from .base_llm import BaseLLM
from .ollama import OllamaLLM
from .openai_llm import OpenAILLM
from .factory import LLMFactory

__all__ = [
    'BaseLLM',
    'OllamaLLM',
    'OpenAILLM',
    'LLMFactory',
]

__version__ = '1.0.0'

