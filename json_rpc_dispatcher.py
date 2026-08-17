from method_handler import list_tools, init, tools_calls_router
from json_rpc_responses import make_json_rpc_responce, make_error_json_rpc_responce, ToolCallError

def dispatch(request: dict) -> dict | None:
    if not isinstance(request, dict):
        return make_error_json_rpc_responce(None, -32600)

    method = request.get('method')
    id = request.get('id')

    if method is None:
        # a response to something we never asked
        return None

    if 'id' not in request: # notification, e.g. notifications/initialized
        return None

    params = request.get('params') or {}

    if method == 'initialize':
        server_init = init(params)
        responce = make_json_rpc_responce(id, server_init)

    elif method == 'ping':
        responce = make_json_rpc_responce(id, {})

    elif method == 'tools/list':
        tool_description = list_tools()
        responce = make_json_rpc_responce(id, tool_description)


    elif method == 'tools/call':
        try:
            tool_call_result = tools_calls_router(params.get('name'), params.get('arguments') or {})

        except ToolCallError as e: # unknown tool / bad arguments
            return make_error_json_rpc_responce(id, e.code)

        except Exception as e: # the tool itself blew up
            return make_json_rpc_responce(id, {
                "content": [{"type": "text", "text": f"Tool execution failed: {e}"}],
                "isError": True
            })

        responce = make_json_rpc_responce(id, {
            "content": [{"type": "text", "text": str(tool_call_result)}],
            "isError": False
        })

    else:
         return make_error_json_rpc_responce(id, -32601)


    return responce