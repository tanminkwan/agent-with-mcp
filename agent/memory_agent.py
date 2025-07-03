# use context7
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
        # LangChain ConversationChain이 자동으로 히스토리 누적 및 프롬프트 생성
        response = self.chain.run(user_input)
        # 프롬프트 로그 출력 (memory의 대화 내용)
        print("\n===== LLM에 전달되는 프롬프트(메모리 기준) =====\n" + str(self.memory.buffer) + "\n==============================\n")
        return response 