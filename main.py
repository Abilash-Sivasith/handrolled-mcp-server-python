"""
Hand Rolled MCP server without any framework
"""
import sys

from transport.transport import Transport
from transport.stdio import StdioTransport

from json_parser import json_parser
from json_rpc_dispatcher import dispatch
from json_rpc_responses import make_error_json_rpc_responce

class MCPServer:
    def __init__(self, transport: Transport):
        self.transportProtocol = transport

def main():

    print("---------------- Hand Rolled MCP Server Started ----------------", file=sys.stderr)
    communication_protocol = StdioTransport()
    mcp_server = MCPServer(communication_protocol)
    # TODO: implement a logger
    while True:
        raw_input = mcp_server.transportProtocol.recieve()
        if raw_input is None:
            break
        try:
            json_inputs = json_parser(raw_input)
        except Exception as e:
            print(f"Error parsing input: {e}", file=sys.stderr)
            continue

        try:
            responce = dispatch(json_inputs) # returns json-rpc message, or None for notifications
        except Exception as e:
            # one bad message must not end the session -- answer with an internal error and carry on
            print(f"Error dispatching request: {e}", file=sys.stderr)
            id = json_inputs.get('id') if isinstance(json_inputs, dict) else None
            if id is not None:
                mcp_server.transportProtocol.send(make_error_json_rpc_responce(id, -32603))
            continue

        if responce is not None:
            mcp_server.transportProtocol.send(responce)



if __name__ == '__main__':
    main()