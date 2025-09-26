import json
import requests

url = "http://localhost:8000/mcp"


headers = {
    "Accept": "application/json,text/event-stream",
}


body_tools_list = {
    "jsonrpc": "2.0",
    "method": "tools/list",
    "id": 1,
    "params": {}
}

body_tools_call = {
    "jsonrpc": "2.0",
    "method": "tools/call",
    "id": 1,
    "params":
      {"name": "subtraction",
        "arguments": {"a": 300, "b": 200}
        }
}

body_list_resources = {
    "jsonrpc": "2.0",
    "method": "resources/list",
    "id": 1,
    "params": {}
}

body_read_resources = {
  "jsonrpc": "2.0",
  "id": 1,
  "method": "resources/read",
  "params": {
    "uri": "file:///myResources/my_python.py"
  }
}
result = requests.post(url, headers=headers, json=body_read_resources)


response = result.text


print(response)
