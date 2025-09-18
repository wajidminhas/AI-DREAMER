

import requests

url = "http://localhost:8000/mcp"

headers = {
    "Accept": "application/json, text/event-stream"}


body = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/call",
    "params": {
        "name": "Addition Tool",
        "arguments": {"a": 1, "b": 2}
    }
}

result = requests.post(url=url, headers=headers, json=body)

print(result.text)