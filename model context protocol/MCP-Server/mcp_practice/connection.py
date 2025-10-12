import asyncio

from mcpClinet.mcp_client import MCPClient

async def main():
    async with MCPClient("http://localhost:8000/mcp") as client:
        res = await client.plus_method(tool_name="addition", a=5, b=3)
        # print (res.contents[0].text)
        print(res.content[0].text)

asyncio.run(main())