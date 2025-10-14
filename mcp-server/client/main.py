#!/usr/bin/env python3
import asyncio
import sys
from pathlib import Path
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    """MCP 클라이언트를 실행하고 서버의 pay 툴을 테스트합니다."""
    # 서버 경로를 절대 경로로 지정
    server_path = Path(__file__).parent.parent / "server" / "main.py"
    
    print(f"🚀 MCP 서버 시작 중...")
    print(f"   서버 경로: {server_path}")
    print()
    
    # 서버 파라미터 설정
    server_params = StdioServerParameters(
        command=sys.executable,  # 현재 Python 인터프리터 사용
        args=[str(server_path)]
    )
    
    try:
        # 서버에 연결
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                # 서버 초기화
                await session.initialize()
                print("✅ 서버 연결 성공!")
                print()
                
                # 툴 목록 조회
                tools = await session.list_tools()
                print("📋 사용 가능한 툴:")
                for tool in tools.tools:
                    print(f"   - {tool.name}: {tool.description}")
                print()
                
                # pay 툴 호출
                test_command = "돈 12345 지불해"
                print(f"💰 테스트 명령 실행: '{test_command}'")
                result = await session.call_tool("pay", {"command": test_command})
                
                print()
                print("📤 서버 응답:")
                print(f"   result 타입: {type(result)}")
                print(f"   result 내용: {result}")
                
                if hasattr(result, 'content'):
                    print(f"   content 개수: {len(result.content)}")
                    for i, content in enumerate(result.content):
                        print(f"   content[{i}] 타입: {type(content)}")
                        if hasattr(content, 'text'):
                            print(f"   {content.text}")
                        else:
                            print(f"   {content}")
                else:
                    print(f"   result에 content 속성이 없습니다.")
                
                print()
                print("✨ 테스트 완료!")
                
    except Exception as e:
        print(f"❌ 에러 발생: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main()) 