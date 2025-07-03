import streamlit as st
from agent.memory_agent import MemoryAgent
from llm.ollama import OllamaLLM

model="gemma3n:e4b"

def run():
    st.title(f"Ollama Chatbot")
    if "agent" not in st.session_state:
        llm = OllamaLLM(model=model)
        st.session_state["agent"] = MemoryAgent(llm.llm)
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