from method_handler import list_tools

def dispatch(request: dict) -> function:
    method = request['method']
    id = request['id']

    if method == 'initalize':
        pass
    elif method == 'tools/list':
        tool_description = list_tools()
        responce = make_json_rpc_responce(id, tool_description)

    elif method == 'tools/call':
        pass
    else:        
        return {
            "jsonrpc": "2.0",
            "id": 1,
            "error": {
                "code": -32601,
                "message": "Method not found"
            }
        }
    
    return responce

def make_json_rpc_responce(id: int, result):
    json_rpc_responce = {
        'jsonrpc': '2.0',
        'id': {id},
        'result': {result}
    }
    return json_rpc_responce