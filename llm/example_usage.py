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
    """Graph 기반 Agent 사용 예제"""
    print("\n=== Graph 기반 Agent 사용 예제 ===")
    from agent.graphs.factory import create_from_env
    from agent.memory_agent import MemoryAgent

    graph_name = os.getenv('AGENT_GRAPH', 'purchase')
    print(f"그래프 선택: {graph_name}")
    graph = create_from_env()
    agent = MemoryAgent(graph)

    response = agent.chat("돈 12345 지불해")
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
    print("   AGENT_GRAPH=purchase python llm/example_usage.py")


if __name__ == "__main__":
    main()

