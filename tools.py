import math
from tool_decorator import tool


@tool()
def add(a, b):
    return a + b

@tool()
def secret_function(a, b):
    return ((a + b) ** a) // b

# instead of the @tool() we can do the following which is equivalent
def is_fibonacci_number(a):
    # TODO: this logic is wrong
    return int((math.sqrt((5 * (a ** 2) + 4)))).is_integer() or int((math.sqrt((5 * (a ** 2) - 4)))).is_integer()

is_fibonacci_number = tool()(is_fibonacci_number)

@tool()
def glaze():
    return "Abilash is pretty cool and 6ft"

