"""
Hand Rolled MCP server without any framework
"""
from transport.transport import Transport
from transport.stdio import StdioTransport
from json_parser import json_parser

class MCPServer:
    def __init__(self, transport: Transport):
        self.transportProtocol = transport

def main():

    print("------------------------------------- Hand Rolled MCP Server Started -------------------------------------")
    communication_protocol = StdioTransport()
    mcp_server = MCPServer(communication_protocol)

    while True:
        raw_input = mcp_server.transportProtocol.recieve()
        if raw_input is None:
            break
        else:
            try:
                json_inputs = json_parser(raw_input)
            except Exception as e:
                print(f"Error parsing input: {e}")

