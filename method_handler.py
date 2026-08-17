import json
import time
from pathlib import Path

from jsonschema import validate, exceptions

from json_rpc_responses import ToolCallError
from tools import add, secret_function, is_fibonacci_number, glaze
from tool_decorator import tool_registry
from logger import log, short

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

    client = params.get('clientInfo') or {}
    log.info(
        "initialize: client=%s v%s, protocol requested=%s negotiated=%s",
        client.get('name', 'unknown'), client.get('version', '?'), requested, negotiated
    )

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

    # the registry is keyed by tool name for lookup; tools/list wants a plain array
    return {"tools": list(tool_registry.values())}

def tools_calls_router(tool_name, arguments):
    tool_description = list_tools()
    tools_by_name = {tool['name']: tool for tool in tool_description['tools']}

    log.tool("call %s(%s)", tool_name, short(arguments))

    if tool_name not in tools_by_name:
        log.error("unknown tool: %s", tool_name)
        raise ToolCallError(-32602)

    tool_schema = tools_by_name[tool_name]['inputSchema']
    try:
        validate(instance=arguments, schema=tool_schema)
    except exceptions.ValidationError as e:
        log.error("invalid arguments for %s: %s", tool_name, e.message)
        raise ToolCallError(-32602)

    started = time.perf_counter()
    result = TOOL_HANLDER[tool_name](**arguments)
    elapsed_ms = (time.perf_counter() - started) * 1000

    log.tool("done %s -> %s (%.1f ms)", tool_name, short(result), elapsed_ms)
    return result

