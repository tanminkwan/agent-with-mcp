## Agenda

### 1. 선수 과정
- llm 기초
    - Neural Network 이해하기
    - Transform model 이해하기
    - tokenize 와 vectorize 이해하기
    - prompt를 처리할 때 llm 이 처리하는 영역과 agent 가 처리하는 영역을 구분
- python 기초
    - python 개발 환경 설치 및 사용 방법
    - langchain 활용에 필요한 기술
    - streamlit 기초
- Cloud(SCP) 기초
    - SCP(v2) 권한 부여
    - 기본 활용(Network 환경 구성, Virtual 서버 생성)
- git 기초
    - git 활용 기본
- Container 기술 기초
    - docker 기본
- Code Agent 활용
    - AI Pro, cursor, Cline 등

### 2. 개발 방법론 (또는 approach)
- Prompt-driven
    - 99% vide coding 으로 진행
    - Code Agent 사용 (AI Pro, Cursor 등)
- Graph-driven
    - Agent 설계 시 node & edge 로 설계하고 소통함
- Ops
    - CI/CD : git, docker 사용한 자동 배포

### 3. Framework
- Langchain
    - LLM Agent를 만들기 위한 Framework
- Langsmith
    - LLM & Agent debugging
- Langraph
    - Graph 관점의 사고
    - RAG, Agent, MCP client 등이 하나의 node 로 구성
    - Graph 시각화 및 소통

### 4. MCP (Model Context Protocol)
- Client :
    - multi mcp server 탑제 가능
- Server : 
    - SSE(Server-Sent-Event) 방식
        - 실습 내용 : ElasticSearch 에서 쿼리를 받아 처리 결과를 보내는 MCP 서버 만들기
    - STDIO 방식
        - 실습 내용 : <구상중 : 로컬 pc의 ollama가 서빙하는 model을 바꾼다던지... >

### 5. RAG
- RAG (Vector-based RAG)
    - 한국어 친화적 embedding 모델 사용
    - 의미 검색
    - 채팅 내용을 요약하여 저장, 이전 행위를 재사용 (나중에 마치 Agent 과거 사건을 기억하는 느낌 구현)
    - Vector DB : Qdrant (SCP 에서 서빙)
- GraphRAG
    - 채팅이 끝났을 때 LLM이 채팅 내용을 분석하여 node 와 edge(관계) 생성 또는 관계의 가중치 변경
    - user 가 질의 시 연관 지식을 조회
    - Graph DB : FalKorDB (llm 친화적) (SCP 에서 서빙)

### 6. llm 서빙
- local(pc) 에 서빙
    - 사용할 기술 : ollama
    - 사용할 모델 : pc에서 동작 가능한 모델들(7b 미만 4bit 양자화 모델등)
    - 체험할 내용 : 양자화 모델, 증류 모델 사용해 보기
- 외부 서비스 사용
    - api key 로 chatgpt 등 외부 초대형 모델 사용 (해당 서비스 구독 필요)
- 직접 서빙하기
    - 사용할 기술 : A100 GPU 서버(SCP 사용), vllm(llm 서빙 도구)
    - 사용할 모델 : 16b 미만 모델들
    - 체험할 내용 : 모델의 정밀도 낮추기, Paged Attention으로 메모리 아끼기

결과적으로 참여자들 각각이 하나의 Project를 완성하는 방식
체험형(구경), 참여형(직접 실습) 두가지 트랙 고려