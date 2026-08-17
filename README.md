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

# Logging

The server logs what it's doing to **stderr** — stdout is reserved for JSON-RPC, so
writing logs there would corrupt the protocol stream. Running in a terminal you'll see
the log inline; under the MCP Inspector it shows up in the Inspector's server log pane.

Levels, lowest to highest:

| Level | What it shows |
|---|---|
| `DEBUG` | raw wire traffic — every line in and out |
| `INFO` | server lifecycle, and each JSON-RPC method as it arrives |
| `TOOL` | tool invocations: name, arguments, result, and how long it took |
| `ERROR` | parse failures, unknown methods/tools, invalid arguments, tools that raised |

`TOOL` is a custom level sitting between `INFO` and `WARNING`, so `MCP_LOG_LEVEL=TOOL`
shows tool calls and errors without the rest of the method chatter.

```
00:28:19 INFO  request: tools/call (id=3)
00:28:19 TOOL  call add({'a': 2, 'b': 3})
00:28:19 TOOL  done add -> 5 (0.0 ms)
00:28:19 INFO  request: tools/call (id=4)
00:28:19 TOOL  call add({'a': 'two', 'b': 3})
00:28:19 ERROR invalid arguments for add: 'two' is not of type 'number'
```

Set the level with the `MCP_LOG_LEVEL` environment variable (default `INFO`; an
unrecognised name falls back to `INFO`):

```bash
MCP_LOG_LEVEL=DEBUG python3 main.py
```

Levels are colour-coded when stderr is a terminal. Set `NO_COLOR` to turn that off.

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
logger.py                # stderr logger (INFO / TOOL / ERROR levels)
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
