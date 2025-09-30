
import resource
from mcp import ClientSession
from typing import Optional
from contextlib import AsyncExitStack
import asyncio
from mcp.client.streamable_http import streamablehttp_client

class MCPClient:
    def __init__(self, url: str):
        self.session : Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        self.url = url


# " this is an async context manager "
    async def __aenter__(self):
        print("Entering the session")
        read, write, _ = await self.exit_stack.enter_async_context(streamablehttp_client(self.url))
        self.session = await self.exit_stack.enter_async_context(ClientSession(read, write))
        await self.session.initialize()
        return self
    

# " this is an async context manager  with exit function "
    async def __aexit__(self, *arg):
        print("Exiting the session")
        await self.exit_stack.aclose()


    async def my_tool_details(self):
        response = await self.session.list_tools()
        tools = response.tools
        print("\nConnected to server with tools:", [tool.name for tool in tools])

    async def my_resource_details(self):
        response = await self.session.list_resources()
        resources = response.resources
        print("\nConnected to server with resources:", [resource.name for resource in resources])

    async def read_my_resource(self, resource_uri: str):
        if self.session is None:
            raise Exception("Session not initialized. Please use 'async with' to create a session.")
        response = await self.session.read_resource(resource_uri)
        return response

    async def list_resource_templates(self):
        if self.session is None:
            raise Exception("Session not initialized. Please use 'async with' to create a session.")
        response = await self.session.list_resource_templates()
        resources = response.resourceTemplates
        print("\nResource templates available:", [resource.name for resource in resources])
        # return resources

    async def plus_method(self, tool_name: str, a: int, b: int):
        if self.session is None:
            raise Exception("Session not initialized. Please use 'async with' to create a session.")
        response = await self.session.call_tool(tool_name, {"a": a, "b": b})
        return response



