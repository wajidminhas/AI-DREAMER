from mcp.server.fastmcp import FastMCP
from mcpTool.mcp_tool import plus_tool, minus_tool
from myResources.my_resouce_method import read_docs, read_docs_dynamic


app = FastMCP(name = "mcp-practice", stateless_http = True)

@app.tool()
async def addition(a: int, b: int) -> str:
    """Add two integers / addition tool, returns the sum of a and b / addition(a, b)"""
    return plus_tool(a, b)


@app.tool()
async def subtraction(a: int, b: int) -> str:
    """Subtract two integers / subtraction tool, returns the difference of a and b / subtraction(a, b)"""
    return minus_tool(a, b)

@app.resource("file:///myResources/my_python.py", mime_type="text/x-python")
async def read_file():
    """Read the content of my_python.py file"""
    return read_docs()

@app.resource("file:///myResources/{path}", mime_type="text/plain")
async def read_file_dynamic(path: str):
    """Read the content of a file given its path"""
    return read_docs_dynamic(path)

mcp_app = app.streamable_http_app()
