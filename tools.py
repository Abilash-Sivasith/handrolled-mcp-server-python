import math
from tool_decorator import tool


@tool()
def add(a: float, b: float):
    """Add two numbers together and return their sum."""
    return a + b

@tool()
def secret_function(a: int, b: int):
    """
    Computes ((a + b) raised to the power of a), then floor-divides the result by b.

    Both a and b should be integers, and b must not be zero.
    """
    return ((a + b) ** a) // b

# instead of the @tool() we can do the following which is equivalent
def is_fibonacci_number(a: int):
    """
    Determines whether a given integer is a Fibonacci number, using the identity that
    n is a Fibonacci number if and only if 5n^2 + 4 or 5n^2 - 4 is a perfect square.
    """
    x, y = 5 * (a ** 2) + 4, 5 * (a ** 2) - 4
    return math.isqrt(x) ** 2 == x or (y >= 0 and math.isqrt(y) ** 2 == y)

is_fibonacci_number = tool()(is_fibonacci_number)

@tool()
def glaze():
    """Returns a short compliment about Abilash, the author of this server. Takes no input."""
    return "Abilash is pretty cool and 6ft"

