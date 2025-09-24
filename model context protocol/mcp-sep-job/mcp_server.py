
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

@app.resource('file:///docs/python_docs.py', name="python_docs")
def read_data_from_file():
    """Read data from a local file"""
    with open("docs/python_docs.py") as f:
        content = f.read()  
        return content

mcp_app = app.streamable_http_app()