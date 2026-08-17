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

def tool():
    def dec(func):
        sig = inspect.signature(func)
        print(sig)
        tool_registry[func.__name__] = {
            "name": func,
            "description": inspect.getdoc(func) or "",
            'inputSchema': ""
        }
        return func

    return dec

def build_input_schema(signature):
    properties = {}
    required = []

    for parameter in signature.parameters.values():
        json_type = {
            int: "integer",
            float: "number",
            str: "string",
            bool: "boolean",
        }.get(parameter.annotation, "string")

        properties[parameter.name] = {
            "type": json_type
        }

        if parameter.default is inspect.Parameter.empty:
            required.append(parameter.name)
        else:
            properties[parameter.name]["default"] = parameter.default

    return {
        "type": "object",
        "properties": properties,
        "required": required,
    }