"""
메인 애플리케이션 진입점
그래프 선택은 .env의 AGENT_GRAPH로 제어합니다.
각 노드에서 사용할 LLM은 .env의 전역/노드별 설정을 통해 선택됩니다.
"""
import os
from dotenv import load_dotenv
from agent.memory_agent import MemoryAgent
from agent.graphs.factory import create_from_env
from ui.streamlit_ui import run

load_dotenv()  # .env 파일에서 환경 변수 로드

# 그래프 선택 및 에이전트 생성
graph = create_from_env()
agent = MemoryAgent(graph)

print(f"🕸️ 사용 중인 그래프: {os.getenv('AGENT_GRAPH', 'purchase')}")

if __name__ == "__main__":
    run() 