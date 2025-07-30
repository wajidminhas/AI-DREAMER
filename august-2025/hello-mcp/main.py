
from mcp.server.fastmcp import FastMCP

mcp = FastMCP(name = "hello-mcp", statlesshttp = True)

mcp_app = mcp.streamable_http_app()

