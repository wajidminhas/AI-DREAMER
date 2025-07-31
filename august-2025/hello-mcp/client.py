import requests

url = "http://localhost:8000/mcp/"  # Update to correct endpoint if needed

headers = {
    "Content-Type": "application/json",
    "Accept": "application/json,text/event-stream"
    # "X-Session-ID": "your-session-id-here"  # Uncomment if server expects session ID in headers
}

body = {
    "jsonrpc": "2.0",
    "method": "tool/list",
    "id": 1,
    "params": {}
    #     "session_id": "your-session-id-here"  # Replace with actual session ID
    # }
}

response = requests.post(url, json=body, headers=headers)

# Handle JSON response directly (no streaming needed for JSON-RPC)
for line in response.iter_lines():
    if line:
        print(line)
# if response.status_code == 200:
#     print(response.json())
# else:
#     print(f"Error: {response.status_code} - {response.text}")