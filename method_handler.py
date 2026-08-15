import json

SUPPORTED_VERSIONS = '2025-11-25'

def init(id: int):
    return {
        "protocolVersion": SUPPORTED_VERSIONS,
        "capabilities": {
            "tools": {
                "listChanged": False
            }
        },
        "serverInfo": {
            "name": "Custom Handrolled MCP Server",
            "version": "1.0.0"
        }
    }

def list_tools():
    with open('tools_description.json', 'r') as file:
        data = json.load(file) 
    return data

def tools_calls_router():
    pass
