#!/usr/bin/env python3
import asyncio
import re
from datetime import datetime
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# 서버 인스턴스 생성
app = Server("pay-server")

@app.list_tools()
async def list_tools() -> list[Tool]:
    """사용 가능한 툴 목록을 반환합니다."""
    return [
        Tool(
            name="pay",
            description="돈 OO 지불해 명령을 받아, OO 금액만큼 지불했다고 응답합니다.",
            inputSchema={
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "예: 돈 10000 지불해"
                    },
                },
                "required": ["command"],
            },
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """툴을 실행하고 결과를 반환합니다."""
    if name == "pay":
        command = arguments.get("command", "")
        match = re.search(r"돈\s*(\d+)\s*지불해", command)
        
        if not match:
            return [TextContent(
                type="text",
                text="❌ 명령이 올바르지 않습니다. 예: 돈 10000 지불해"
            )]
        
        amount = int(match.group(1))
        paid_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        result = f"✅ 지불 완료!\n금액: {amount:,}원\n시각: {paid_at}"
        
        return [TextContent(
            type="text",
            text=result
        )]
    
    raise ValueError(f"Unknown tool: {name}")

async def main():
    """서버를 실행합니다."""
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )

if __name__ == "__main__":
    asyncio.run(main()) 