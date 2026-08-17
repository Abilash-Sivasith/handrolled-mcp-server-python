# handrolled-mcp-server-python
Building an basic MCP server without any framework

A minimal implementation of the [Model Context Protocol](https://modelcontextprotocol.io) server, built from scratch in Python with no MCP SDK — just raw JSON-RPC 2.0 message handling over stdio. It's a learning project for understanding how MCP works under the hood.

# Requirements

- Python 3.10+
- [`jsonschema`](https://pypi.org/project/jsonschema/) (used to validate tool call arguments against each tool's input schema)

Install the dependency:

```bash
pip install jsonschema
```

# How to Run

Run main.py in a terminal:

```bash
python3 main.py
```

The server communicates over stdio: it reads one JSON-RPC 2.0 message per line from stdin and writes responses to stdout. Notifications (messages with no `id`, e.g. `notifications/initialized`) are handled silently and never produce a response, per the JSON-RPC spec.

Supported methods:

- `initialize` — returns protocol version, capabilities, and server info
- `tools/list` — returns the tool catalog (see [tools_descriptions.json](tools_descriptions.json))
- `tools/call` — invokes a tool by name with arguments, validated against its JSON schema

# How to test

## MCP Inspector

Use the official [MCP Inspector](https://github.com/modelcontextprotocol/inspector) to interact with the server through a web UI:

```bash
npx @modelcontextprotocol/inspector python3 main.py
```

This launches the server as a subprocess over stdio and opens a browser UI where you can call `initialize`, `tools/list`, and `tools/call` manually.

## Connecting to a MCP client

Point any stdio-based MCP client (e.g. Claude Desktop) at `main.py` by adding it to the client's server config:

```json
{
  "mcpServers": {
    "handrolled-mcp-server": {
      "command": "python3",
      "args": ["/absolute/path/to/main.py"]
    }
  }
}
```

## Manual testing

Since the server just reads JSON-RPC lines from stdin, you can also drive it by hand in a terminal:

```
python3 main.py
{"jsonrpc": "2.0", "id": 1, "method": "initialize"}
{"jsonrpc": "2.0", "id": 2, "method": "tools/list"}
{"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "add", "arguments": {"a": 2, "b": 3}}}
```

Type (or paste) one line at a time and press enter; the corresponding response is printed to stdout. Press `Ctrl+C` to stop the server.

# Available Tools

| Tool | Description |
|---|---|
| `add` | Add two numbers together and return their sum. |
| `secret_function` | Computes `((a + b) ** a) // b`. |
| `is_fibonacci_number` | Determines whether a given integer is a Fibonacci number. |
| `glaze` | Returns a short compliment about MCP. Takes no input. |

Full schemas for each tool live in [tools_descriptions.json](tools_descriptions.json).

# Project Structure

```
main.py                  # entry point, read/dispatch/send loop
json_parser.py           # raw string -> dict
json_rpc_dispatcher.py   # routes JSON-RPC methods to handlers
json_rpc_responses.py    # JSON-RPC result/error message builders
method_handler.py        # initialize / tools/list / tools/call logic
tools.py                 # tool implementations
tools_descriptions.json  # tool catalog + input schemas (MCP tools/list)
transport/
  transport.py           # abstract Transport interface
  stdio.py                # stdio implementation of Transport
```

# License

MIT — see [LICENSE](LICENSE).
