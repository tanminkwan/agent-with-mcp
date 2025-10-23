"""
Streamlit UI 모듈
그래프 기반 에이전트를 사용하여 대화 흐름을 제어한다.
그래프 선택은 .env의 AGENT_GRAPH로 제어한다.
"""
import os
import streamlit as st
from agent.memory_agent import MemoryAgent
from agent.graphs.factory import create_from_env


def run():
    graph_name = os.getenv('AGENT_GRAPH', 'purchase')
    st.title("🤖 Graph-driven Chatbot")
    st.caption(f"현재 그래프: {graph_name}")
    
    # Agent 초기화 (세션 상태에 저장)
    if "agent" not in st.session_state:
        try:
            graph = create_from_env()
            st.session_state["agent"] = MemoryAgent(graph)
        except Exception as e:
            st.error(f"❌ 그래프 초기화 실패: {e}")
            st.stop()
    
    agent = st.session_state["agent"]
    if "messages" not in st.session_state:
        st.session_state["messages"] = []
    for msg in st.session_state["messages"]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
    user_input = st.chat_input("메시지를 입력하세요...")
    if user_input:
        st.session_state["messages"].append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)
        bot_response = agent.chat(user_input)
        st.session_state["messages"].append({"role": "assistant", "content": bot_response})
        with st.chat_message("assistant"):
            st.markdown(bot_response) 