"""
LLM 모듈 사용 예제

이 파일은 추상화 계층을 사용하여 Ollama와 OpenAI를 
어떻게 선택적으로 사용하는지 보여줍니다.
"""
import os
from llm import LLMFactory


def example_ollama():
    """Ollama 사용 예제"""
    print("\n=== Ollama 사용 예제 ===")
    
    # Ollama LLM 생성
    llm = LLMFactory.create(
        provider='ollama',
        model='llama2',
        temperature=0.7
    )
    
    print(f"생성된 LLM: {llm.__class__.__name__}")
    print(f"모델명: {llm.get_model_name()}")
    print(f"설정: {llm.get_config()}")
    
    # LangChain과 함께 사용
    from langchain.schema import HumanMessage
    message = HumanMessage(content="안녕하세요!")
    response = llm([message])
    print(f"응답: {response.content}")


def example_openai():
    """OpenAI 사용 예제"""
    print("\n=== OpenAI 사용 예제 ===")
    
    # 환경변수 확인
    if not os.getenv('OPENAI_API_KEY'):
        print("⚠️  OPENAI_API_KEY 환경변수가 설정되지 않았습니다.")
        print("export OPENAI_API_KEY='your-api-key' 명령으로 설정하세요.")
        return
    
    # OpenAI LLM 생성
    llm = LLMFactory.create(
        provider='openai',
        model='gpt-4',
        temperature=0.7,
        max_tokens=100
    )
    
    print(f"생성된 LLM: {llm.__class__.__name__}")
    print(f"모델명: {llm.get_model_name()}")
    print(f"설정: {llm.get_config()}")
    
    # LangChain과 함께 사용
    from langchain.schema import HumanMessage
    message = HumanMessage(content="안녕하세요!")
    response = llm([message])
    print(f"응답: {response.content}")


def example_with_agent():
    """Agent와 함께 사용하는 예제"""
    print("\n=== Agent와 함께 사용 예제 ===")
    
    # 환경변수나 설정으로 제공자 선택
    provider = os.getenv('LLM_PROVIDER', 'ollama')  # 기본값: ollama
    model = os.getenv('LLM_MODEL', 'llama2')        # 기본값: llama2
    
    print(f"선택된 제공자: {provider}")
    print(f"선택된 모델: {model}")
    
    # Factory를 통해 LLM 생성
    if provider == 'openai' and not os.getenv('OPENAI_API_KEY'):
        print("⚠️  OPENAI_API_KEY가 필요합니다. Ollama로 전환합니다.")
        provider = 'ollama'
        model = 'llama2'
    
    llm = LLMFactory.create(provider=provider, model=model)
    
    # MemoryAgent와 함께 사용
    from agent.memory_agent import MemoryAgent
    agent = MemoryAgent(llm)
    
    response = agent.chat("파이썬이란 무엇인가요?")
    print(f"\nAgent 응답: {response}")


def show_available_providers():
    """사용 가능한 제공자 목록 출력"""
    print("\n=== 사용 가능한 LLM 제공자 ===")
    providers = LLMFactory.get_available_providers()
    for provider in providers:
        print(f"- {provider}")


def main():
    """메인 함수"""
    print("🚀 LLM 추상화 계층 사용 예제\n")
    print("SOLID 원칙을 적용한 LLM 모듈 데모")
    
    # 사용 가능한 제공자 확인
    show_available_providers()
    
    # 각 제공자별 예제 (주석 해제하여 사용)
    # example_ollama()
    # example_openai()
    
    # Agent와 함께 사용하는 예제
    # example_with_agent()
    
    print("\n✅ 예제 완료!")
    print("\n💡 사용 방법:")
    print("   LLM_PROVIDER=ollama LLM_MODEL=llama2 python llm/example_usage.py")
    print("   LLM_PROVIDER=openai LLM_MODEL=gpt-4 OPENAI_API_KEY=sk-... python llm/example_usage.py")


if __name__ == "__main__":
    main()

