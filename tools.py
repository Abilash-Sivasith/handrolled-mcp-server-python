import math

def add(a, b):
    return a + b

def secret_function(a, b):
    return ((a + b) ** a) // b

def is_fibonacci_number(a):
    return int((math.sqrt((5 * (a ** 2) + 4)))).is_integer() or int((math.sqrt((5 * (a ** 2) - 4)))).is_integer()

def glaze():
    return "Learning about MCP is fun"

