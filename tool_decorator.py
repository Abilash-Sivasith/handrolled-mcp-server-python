"""
Use the tools docstring to generate tool descriptions 
and creating a deocrated @tool() to auto add a new tool to add it to the registry
"""

"""
An example of a registered tool in the tool_registry


    {
      "name": "add",
      "description": "Add two numbers together and return their sum.",
      "inputSchema": {
        "type": "object",
        "properties": {
          "a": {
            "type": "number",
            "description": "The first addend."
          },
          "b": {
            "type": "number",
            "description": "The second addend."
          }
        },
        "required": ["a", "b"]
      },
      "annotations": {
        "title": "Add",
        "readOnlyHint": true,
        "destructiveHint": false,
        "idempotentHint": true,
        "openWorldHint": false
      }
    },

"""


import inspect

tool_registry = {}

JSON_TYPES = {
    int: "integer",
    float: "number",
    str: "string",
    bool: "boolean",
}

def tool():
    def dec(func):
        sig = inspect.signature(func)
        tool_registry[func.__name__] = {
            "name": func.__name__,
            "description": inspect.getdoc(func) or "",
            'inputSchema': build_input_schema(sig)
        }
        return func

    return dec

def build_input_schema(signature):
    properties = {}
    required = []

    for parameter in signature.parameters.values():
        # an unannotated parameter is left untyped -- guessing "string" would make the
        # schema reject calls the tool would happily accept
        parameter_schema = {}
        if parameter.annotation in JSON_TYPES:
            parameter_schema["type"] = JSON_TYPES[parameter.annotation]

        properties[parameter.name] = parameter_schema

        if parameter.default is inspect.Parameter.empty:
            required.append(parameter.name)
        else:
            parameter_schema["default"] = parameter.default

    return {
        "type": "object",
        "properties": properties,
        "required": required,
    }