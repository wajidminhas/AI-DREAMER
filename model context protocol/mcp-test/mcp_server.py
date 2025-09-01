
from mcp.server.fastmcp import FastMCP

mcp_app = FastMCP(name="MCP Server", stateless_http=True)


docs = {
    "Introduction": "This is a sample MCP server implementation using FastMCP.",
    "ReadMe": "This server provides a list of tools and resources.",
    "Contact": "For more information, visit https://fastmcp.com",
}

def list_docs():
    """Returns the documentation dictionary."""
    print("Listing docs...")
    print(f"list {(docs.keys())}") 

    print("Docs listed.")
    

print("Docs: ", docs)
    
    
     
    
mcp_ser = mcp_app.streamable_http_app()