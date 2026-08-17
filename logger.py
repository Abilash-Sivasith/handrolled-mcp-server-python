"""
Logging for the server.

Everything is written to stderr on purpose: stdout is the JSON-RPC channel, so
anything printed there that isn't a protocol message corrupts the stream and the
client drops the connection. stderr is free, and stdio MCP clients (the Inspector,
Claude Desktop) surface it as the server log.

Levels, lowest to highest:

    DEBUG   raw wire traffic -- every line in and out
    INFO    lifecycle and each JSON-RPC method that comes in
    TOOL    tool invocations: name, arguments, result, how long it took
    ERROR   parse failures, unknown methods/tools, tools that blew up

TOOL sits above INFO so `MCP_LOG_LEVEL=TOOL` shows tool calls and errors without
the rest of the method chatter.

Usage:

    from logger import log

    log.info("...")
    log.tool("...")
    log.error("...")

The level is read from the MCP_LOG_LEVEL environment variable (default INFO), and
colour is used when stderr is a terminal unless NO_COLOR is set.
"""

import logging
import os
import sys

# between INFO (20) and WARNING (30)
TOOL = 25
logging.addLevelName(TOOL, "TOOL")

RESET = "\033[0m"
LEVEL_COLOURS = {
    "DEBUG": "\033[90m",     # grey
    "INFO": "\033[36m",      # cyan
    "TOOL": "\033[35m",      # magenta
    "WARNING": "\033[33m",   # yellow
    "ERROR": "\033[31m",     # red
    "CRITICAL": "\033[1;31m",  # bold red
}

# long tool arguments/results would otherwise bury the rest of the log
MAX_VALUE_LENGTH = 300


class MCPLogger(logging.Logger):
    """A stdlib logger with an extra .tool() call for the TOOL level."""

    def tool(self, message, *args, **kwargs):
        if self.isEnabledFor(TOOL):
            self._log(TOOL, message, args, **kwargs)


class ColourFormatter(logging.Formatter):
    def __init__(self, colour: bool):
        super().__init__("%(asctime)s %(levelname)s %(message)s", datefmt="%H:%M:%S")
        self.colour = colour

    def format(self, record):
        original = record.levelname
        # pad first, then wrap -- colour codes are invisible but still count towards
        # the width, so padding afterwards would misalign the columns
        padded = f"{original:<5}"
        if self.colour:
            record.levelname = f"{LEVEL_COLOURS.get(original, '')}{padded}{RESET}"
        else:
            record.levelname = padded
        try:
            return super().format(record)
        finally:
            # records can be handled more than once, so leave it as we found it
            record.levelname = original


def short(value) -> str:
    """Render a value for the log, clipped so one huge payload can't flood the terminal."""
    text = str(value)
    if len(text) > MAX_VALUE_LENGTH:
        return text[:MAX_VALUE_LENGTH] + f"... ({len(text)} chars)"
    return text


def _build_logger() -> MCPLogger:
    logging.setLoggerClass(MCPLogger)
    try:
        logger = logging.getLogger("mcp")
    finally:
        logging.setLoggerClass(logging.Logger)

    level_name = os.environ.get("MCP_LOG_LEVEL", "INFO").upper()
    # getLevelName maps a known name to its int, and returns "Level X" for anything
    # it doesn't recognise -- so a typo falls back to INFO instead of crashing
    level = logging.getLevelName(level_name)
    logger.setLevel(level if isinstance(level, int) else logging.INFO)

    handler = logging.StreamHandler(sys.stderr)
    use_colour = sys.stderr.isatty() and "NO_COLOR" not in os.environ
    handler.setFormatter(ColourFormatter(use_colour))

    logger.addHandler(handler)
    logger.propagate = False  # don't also hand records to the root logger
    return logger


log: MCPLogger = _build_logger()
