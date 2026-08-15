from method_handler import list_tools, init

ERROR_CODES = {
    -32700: "Parse error",
    -32600: "Invalid Request",
    -32601: "Method not found",
    -32602: "Invalid params",
    -32603: "Internal error",
}

def dispatch(request: dict) -> function:
    method = request['method']
    id = request['id']

    if method == 'initalize':
        server_init = init(id)
        responce = make_json_rpc_responce(id, server_init)

    elif method == 'tools/list':
        tool_description = list_tools()
        responce = make_json_rpc_responce(id, tool_description)


    elif method == 'tools/call':
        pass


    else: 
         return make_error_json_rpc_responce(id, -32601)       

    
    return responce

def make_json_rpc_responce(id: int, result):
    json_rpc_responce = {
        'jsonrpc': '2.0',
        'id': {id},
        'result': {result}
    }
    return json_rpc_responce

def make_error_json_rpc_responce(id: int, error_code: int):
        return {
            "jsonrpc": "2.0",
            "id": {id},
            "error": {
                "code": error_code,
                "message": ERROR_CODES[error_code]
            }
        }