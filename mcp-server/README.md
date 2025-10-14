# MCP 서버/클라이언트 실행 가이드

## 1. 의존성 설치

```
pip install -r requirements.txt
```

## 2. 실행 방법

```
python client/main.py
```

- 서버는 자동으로 subprocess로 실행됩니다.
- pay 툴은 "돈 12345 지불해" 명령을 받아 금액/일시를 반환합니다.

## 3. 디렉토리 구조
```
mcp-server/
  ├─ server/
  │    └─ main.py
  ├─ client/
  │    └─ main.py
  └─ requirements.txt
```

## 4. 참고
- MCP 공식 문서: https://github.com/modelcontextprotocol/python-sdk 