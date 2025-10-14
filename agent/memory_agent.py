# use context7
import os
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

system_prompt = """
You are a rational educator.  
• When the user states facts, restate them in one concise sentence.  
• When the user asks a question, answer it directly in one concise sentence.  
Do not add opinions, compliments, or pleasantries.
"""

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")
])

class MemoryAgent:
    def __init__(self, llm):
        self.memory = ConversationBufferMemory(return_messages=True)
        self.chain = ConversationChain(llm=llm, memory=self.memory, prompt=prompt, verbose=True)
    def chat(self, user_input: str) -> str:
        # LangSmith 트레이싱 태그/메타데이터를 포함하여 호출
        invoke_result = self.chain.invoke(
            {"input": user_input},
            config={
                "tags": ["ui", "chat"],
                "metadata": {
                    "component": "MemoryAgent",
                    "llm": str(self.chain.llm),
                },
            },
        )
        # 디버그 로그는 환경변수로 제어
        if os.getenv("DEBUG_PROMPT", "false").lower() in {"1", "true", "yes"}:
            print(
                "\n===== LLM에 전달되는 프롬프트(메모리 기준) =====\n"
                + str(self.memory.buffer)
                + "\n==============================\n"
            )
        # 항상 문자열을 반환하도록 정규화
        if hasattr(invoke_result, "content"):
            return getattr(invoke_result, "content")  # AIMessage 등
        if isinstance(invoke_result, str):
            return invoke_result
        if isinstance(invoke_result, dict):
            for key in ("output", "text", "response", "content"):
                if key in invoke_result and isinstance(invoke_result[key], str):
                    return invoke_result[key]
        return str(invoke_result)