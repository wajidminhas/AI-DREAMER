import asyncio

from mcpClinet.mcp_client import MCPClient

async def main():
    async with MCPClient("http://localhost:8000/mcp") as client:
        res = await client.read_my_resource("file:///myResources/my_python.py")
        print (res)

asyncio.run(main())