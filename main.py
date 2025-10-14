"""
메인 애플리케이션 진입점
환경변수를 통해 LLM 제공자를 선택할 수 있습니다.

환경변수:
- LLM_PROVIDER: 'ollama' 또는 'openai' (기본값: ollama)
- LLM_MODEL: 모델명 (기본값: gemma3n:e4b)
- OPENAI_API_KEY: OpenAI 사용 시 필요

사용 예시:
    python main.py
    LLM_PROVIDER=openai LLM_MODEL=gpt-4 OPENAI_API_KEY=sk-... python main.py
"""
import os
from dotenv import load_dotenv
from llm import LLMFactory
from agent.memory_agent import MemoryAgent
from ui.streamlit_ui import run

load_dotenv()  # .env 파일에서 환경 변수 로드

# 환경변수에서 LLM 설정 읽기
provider = os.getenv('LLM_PROVIDER', 'ollama')
model = os.getenv('LLM_MODEL', 'gemma3n:e4b')

# Factory를 통해 LLM 생성
# SOLID 원칙의 의존성 역전 원칙(DIP) 적용: 구체 클래스가 아닌 추상화에 의존
llm = LLMFactory.create(
    provider=provider,
    model=model,
    temperature=0.7
)

# Agent 생성
# MemoryAgent는 LangChain 모델을 필요로 하므로 as_langchain_model()을 사용
agent = MemoryAgent(llm.as_langchain_model())

print(f"🤖 사용 중인 LLM: {llm.__class__.__name__} ({model})")

if __name__ == "__main__":
    run() 