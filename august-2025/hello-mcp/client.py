import requests

url = "http://localhost:8000/mcp"

headers = {
    
    "Accept": "application/json, text/event-stream"
}

body = {
    "jsonrpc": "2.0",
    "method": "tool/list",
    "params" : {},
    "id": 1
}

