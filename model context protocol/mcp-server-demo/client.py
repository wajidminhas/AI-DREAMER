
import requests

url =  "http://localhost:8000/mcp/"


headers = {
    "Accept": "application/json,text/event-stream"
}

body = {
    "jsonrpc": "2.0",
    "method" : "tools/list",
    "params": {},
    "id": 1
}

response = requests.post(url, json=body, headers=headers)
print(response.text)
# for line in response.iter_lines():

#     if line:
#         print(line)