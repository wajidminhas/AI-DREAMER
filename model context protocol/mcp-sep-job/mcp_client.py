

import requests

url = "http://localhost:8000/mcp"

headers = {
    "Accept": "application/json,text/event-stream"}


body = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "resources/templates/list",
    # "params": {
    #     "uri": "file:///docs/python_docs.py"
    # }
    
}

result = requests.post(url=url, headers=headers, json=body)

print(result.text)