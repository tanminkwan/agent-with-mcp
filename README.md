# SOLID 기반 LangChain + Ollama + Streamlit 챗봇

## 개요
- 이 프로젝트는 SOLID 원칙을 철저히 준수하여 설계된 대화형 챗봇 예제입니다.
- LangChain, Ollama(로컬 LLM), Streamlit을 활용하여 확장성과 유지보수성이 뛰어난 구조를 제공합니다.

## 주요 특징
- **SOLID 원칙 준수**: 단일 책임, 개방/폐쇄, 리스코프 치환, 인터페이스 분리, 의존 역전 원칙 적용
- **모듈화**: LLM, Agent, UI를 각각 분리하여 관리
- **확장성**: 새로운 LLM, Tool, Agent, UI를 쉽게 추가/교체 가능
- **Streamlit UI**: 웹 브라우저에서 바로 대화 가능

## 폴더/파일 구조
```
project/
├─ llm/
│   ├─ base.py           # LLM 추상화(ABC)
│   └─ ollama.py         # Ollama LLM 구현
├─ agent/
│   └─ simple_agent.py   # 단순 에이전트
├─ ui/
│   └─ streamlit_ui.py   # Streamlit UI
├─ main.py               # 전체 조립 및 실행 엔트리포인트
├─ requirements.txt      # 의존성 목록
├─ RULES.md              # 프로젝트 개발 규칙(SOLID 등)
└─ README.md             # (이 문서)
```

## 실행 방법
1. **Ollama 서버 실행**
   ```bash
   ollama serve
   ```
2. **필요시 모델 다운로드 및 로드**
   ```bash
   ollama run gemma3n:e4b
   ```
3. **필요 패키지 설치**
   ```bash
   pip install -r requirements.txt
   ```
4. **Streamlit UI 실행**
   ```bash
   streamlit run main.py
   ```
5. **웹 브라우저에서 접속**
   - http://localhost:8501

## 개발 규칙
- 자세한 내용은 RULES.md 참고
- 모든 코드 설계 및 구현 시 SOLID 원칙을 반드시 준수
- 각 모듈/클래스/함수는 하나의 책임만 갖도록 분리
- 확장에 유연하며, 추상화와 의존성 역전을 적극 활용

## 확장/응용 예시
- context7 등 외부 Tool 연동
- 다양한 LLM/Agent 구조 추가
- LangChain Tool/Memory/Agent 등 고급 기능 적용

---
문의/기여/확장 요청은 언제든 환영합니다! 