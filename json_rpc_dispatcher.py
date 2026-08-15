

def dispatch(request: dict) -> function:
    method = request['method']
    if method == 'initalize':
        pass
    elif method == 'tools/list':
        pass
    elif method == 'tools/call':
        pass
    else:
        raise Exception("Unrecognised method request for mcp client")
