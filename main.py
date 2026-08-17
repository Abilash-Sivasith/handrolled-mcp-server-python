"""
Hand Rolled MCP server without any framework
"""

from transport.transport import Transport
from transport.stdio import StdioTransport

from json_parser import json_parser
from json_rpc_dispatcher import dispatch
from json_rpc_responses import make_error_json_rpc_responce
from logger import log, short

class MCPServer:
    def __init__(self, transport: Transport):
        self.transportProtocol = transport

def main():

    log.info("---------------- Hand Rolled MCP Server Started ----------------")
    communication_protocol = StdioTransport()
    mcp_server = MCPServer(communication_protocol)

    while True:
        raw_input = mcp_server.transportProtocol.recieve()
        if raw_input is None:
            log.info("stdin closed, shutting down")
            break

        log.debug("<-- %s", short(raw_input))

        try:
            json_inputs = json_parser(raw_input)
        except Exception as e:
            log.error("failed to parse input: %s | raw: %s", e, short(raw_input))
            continue

        try:
            responce = dispatch(json_inputs) # returns json-rpc message, or None for notifications
        except Exception:
            # one bad message must not end the session -- answer with an internal error and carry on
            log.exception("dispatch raised while handling the request")
            id = json_inputs.get('id') if isinstance(json_inputs, dict) else None
            if id is not None:
                mcp_server.transportProtocol.send(make_error_json_rpc_responce(id, -32603))
            continue

        if responce is not None:
            log.debug("--> %s", short(responce))
            mcp_server.transportProtocol.send(responce)



if __name__ == '__main__':
    main()
