
from mcp import ClientSession
from contextlib import AsyncExitStack
from mcp.client.streamable_http import streamablehttp_client



class MCPClient:
    def __init__(self, url):
        self.url = url
        self.stack = AsyncExitStack()
        self._sess = None


    async def list_tools(self):
        async with self.session as session:
            response = (await session.list_tools()).tools
            return response
        
    async def __aenter__(self):
        read, write, _ = await self.stack.enter_async_context(
           streamablehttp_client(self.url)
        )
        self._sess = await self.stack.enter_async_context(
            ClientSession(read, write)
        )

        await self._sess.initialize()
        return self
        
    async def __aexit__(self, *args):
        await self.stack.aclose()

    async def list_tools(self):
        return (await self._sess.list_tools()).tools

        
async def main():
    async with MCPClient("http://localhost:8000/mcp") as client:
        tools = await client.list_tools()
        print("TOOLS : ", tools)
        # for tool in tools:
            # print(f"Tool Name: {tool.name}, Description: {tool.description}")
import asyncio
if __name__ == "__main__":
    asyncio.run(main())
