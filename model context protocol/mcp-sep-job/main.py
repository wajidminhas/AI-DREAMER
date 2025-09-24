import asyncio
from my_mcp_client.my_mcp_client import MCPClient


async def main():
    
    async with MCPClient("http://localhost:8000/mcp") as client:
        response = await client.tool_method("plus", {"a": 5, "b": 3})
        print(response)
        
        
    
        
        
asyncio.run(main())