import json
from jsonschema import validate, exceptions

from json_rpc_responses import ToolCallError
from tools import add, secret_function, is_fibonacci_number, glaze

SUPPORTED_VERSIONS = '2025-11-25'

TOOL_HANLDER = {
    'add': add,
    'secret_function': secret_function,
    'is_fibonacci_number': is_fibonacci_number,
    'glaze': glaze

}

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
    with open('tools_descriptions.json', 'r') as file:
        data = json.load(file)
    return data

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

