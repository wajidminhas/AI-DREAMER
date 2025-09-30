import asyncio

from mcpClinet.mcp_client import MCPClient

async def main():
    async with MCPClient("http://localhost:8000/mcp") as client:
        res = await client.list_resource_templates()
        # print (res.contents[0].text)
        print(res)

asyncio.run(main())