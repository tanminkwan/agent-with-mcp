from llm.ollama import OllamaLLM
from agent.memory_agent import MemoryAgent
from ui.streamlit_ui import run

llm = OllamaLLM(model="gemma3n:e4b")
agent = MemoryAgent(llm.llm)

if __name__ == "__main__":
    run() 