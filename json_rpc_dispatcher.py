from method_handler import list_tools, init, tools_calls_router
from json_rpc_responses import make_json_rpc_responce, make_error_json_rpc_responce, ToolCallError

def dispatch(request: dict) -> dict:
    method = request['method']
    id = request['id']

    if method == 'initalize':
        server_init = init(id)
        responce = make_json_rpc_responce(id, server_init)

    elif method == 'tools/list':
        tool_description = list_tools()
        responce = make_json_rpc_responce(id, tool_description)


    elif method == 'tools/call':
        params = request.get('params', {})
        try:
            tool_call_result = tools_calls_router(params.get('name'), params.get('arguments') or {})
        except ToolCallError as e:
            return make_error_json_rpc_responce(id, e.code)
        
        responce = make_json_rpc_responce(id, tool_call_result)

    else: 
         return make_error_json_rpc_responce(id, -32601)       

    
    return responce