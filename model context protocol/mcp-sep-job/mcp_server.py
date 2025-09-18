
from mcp.server.fastmcp import FastMCP


app = FastMCP(name = "mcp_server", stateless_http = True)



@app.tool(name="Addition Tool")
async def too_plus(a: int, b:int)->str:
    """plus two number / plus function tool"""
    return f"you answer is {a+b}"


mcp_app = app.streamable_http_app()