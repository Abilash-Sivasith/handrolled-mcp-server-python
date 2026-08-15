ERROR_CODES = {
    -32700: "Parse error",
    -32600: "Invalid Request",
    -32601: "Method not found",
    -32602: "Invalid params",
    -32603: "Internal error",
}

class ToolCallError(Exception):
    def __init__(self, code: int):
        self.code = code

def make_json_rpc_responce(id: int, result):
    return {
        'jsonrpc': '2.0',
        'id': id,
        'result': result
    }

def make_error_json_rpc_responce(id: int, error_code: int):
    return {
        "jsonrpc": "2.0",
        "id": id,
        "error": {
            "code": error_code,
            "message": ERROR_CODES[error_code]
        }
    }
