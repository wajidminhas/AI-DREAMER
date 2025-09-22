
from mcp.server.fastmcp import FastMCP


app = FastMCP(name = "mcp_server", stateless_http = True)



@app.tool(name="plus")
async def tool_plus(a: int, b:int)->str:
    """plus two number / plus function tool"""
    return f"you answer is {a+b}"

@app.tool(name="subtract")
async def tool_subtract(a: int, b:int)->str:
    """plus two number / plus function tool"""
    return f"you answer is {a-b}"


mcp_app = app.streamable_http_app()