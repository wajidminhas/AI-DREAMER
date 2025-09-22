
from mcp import ClientSession
from typing import Optional
from contextlib import AsyncExitStack
from mcp.client.streamable_http import streamablehttp_client

class MCPClient:
    def __init__(self, url: str):
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        self.url = url
        
        
    async def __aenter__(self):
        print("Entering MCPClient context")
        read, write, _ = await self.exit_stack.enter_async_context(streamablehttp_client(self.url))
        self.session = await self.exit_stack.enter_async_context(ClientSession(read, write))
        await self.session.initialize()
        return self
    
    async def __aexit__(self, *args):
        print("Exiting client context")
        await self.exit_stack.aclose()
        
    async def exist_tool(self):
        response = await self.session.list_tools()
        tools = response.tools
        print("Available tools:")
        [tool.name for tool in tools]      
        
    async def tool_method(self, tool_name: str, agr: dict):
        response = await self.session.call_tool(tool_name, agr) 
        return response 

    async def plus(self):
        return "Plus method called"