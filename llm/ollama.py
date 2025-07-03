from langchain_community.chat_models import ChatOllama

class OllamaLLM:
    def __init__(self, model: str):
        self.llm = ChatOllama(model=model)
    def __call__(self, *args, **kwargs):
        return self.llm(*args, **kwargs) 