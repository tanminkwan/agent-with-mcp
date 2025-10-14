"""
Streamlit UI 모듈
환경변수를 통해 LLM 제공자를 동적으로 선택 가능

SOLID 원칙:
- 의존성 역전 원칙(DIP): 구체 클래스가 아닌 Factory를 통한 추상화 사용
- 단일 책임 원칙(SRP): UI 표시만 담당, LLM 선택은 Factory에 위임
"""
import os
import streamlit as st
from agent.memory_agent import MemoryAgent
from llm import LLMFactory


def run():
    # 환경변수에서 LLM 설정 읽기 (Streamlit 세션에서도 동작)
    provider = os.getenv('LLM_PROVIDER', 'ollama')
    model = os.getenv('LLM_MODEL', 'gemma3n:e4b')
    
    # 타이틀에 현재 사용 중인 LLM 표시
    st.title(f"🤖 Multi-LLM Chatbot")
    st.caption(f"현재 사용 중: {provider.upper()} - {model}")
    
    # Agent 초기화 (세션 상태에 저장)
    if "agent" not in st.session_state:
        try:
            llm = LLMFactory.create(provider=provider, model=model, temperature=0.7)
            st.session_state["agent"] = MemoryAgent(llm.as_langchain_model())
            st.session_state["llm_info"] = f"{llm.__class__.__name__} ({model})"
        except Exception as e:
            st.error(f"❌ LLM 초기화 실패: {e}")
            st.info("💡 Ollama를 사용하는 경우 'ollama serve' 명령으로 서버를 실행하세요.")
            st.info("💡 OpenAI를 사용하는 경우 OPENAI_API_KEY 환경변수를 설정하세요.")
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