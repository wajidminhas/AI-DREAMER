
from mcp.server.fastmcp import FastMCP

mcp_app = FastMCP(name="MCP Server", stateless_http=True)


mcp_ser = mcp_app.streamable_http_app()