import json
from pathlib import Path

from jsonschema import validate, exceptions

from json_rpc_responses import ToolCallError
from tools import add, secret_function, is_fibonacci_number, glaze
from tool_decorator import tool_registry

# newest first, so SUPPORTED_VERSIONS[0] is what we fall back to
SUPPORTED_VERSIONS = [
    '2025-11-25',
    '2025-06-18',
    '2025-03-26',
    '2024-11-05',
]

# resolved against this file, not the cwd, so the server runs from anywhere
TOOLS_DESCRIPTION_PATH = Path(__file__).parent / 'tools_descriptions.json'

TOOL_HANLDER = {
    'add': add,
    'secret_function': secret_function,
    'is_fibonacci_number': is_fibonacci_number,
    'glaze': glaze

}

def init(params: dict):
    requested = params.get('protocolVersion')
    negotiated = requested if requested in SUPPORTED_VERSIONS else SUPPORTED_VERSIONS[0]

    return {
        "protocolVersion": negotiated,
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
    # with open(TOOLS_DESCRIPTION_PATH, 'r') as file:
    #     data = json.load(file)
    # return data
    return tool_registry

def tools_calls_router(tool_name, arguments):
    tool_description = list_tools()
    tools_by_name = {tool['name']: tool for tool in tool_description['tools']}

    if tool_name not in tools_by_name:
        raise ToolCallError(-32602)

    tool_schema = tools_by_name[tool_name]['inputSchema']
    try:
        validate(instance=arguments, schema=tool_schema)
    except exceptions.ValidationError:
        raise ToolCallError(-32602)

    return TOOL_HANLDER[tool_name](**arguments)

