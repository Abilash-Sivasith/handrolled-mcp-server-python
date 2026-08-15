import json

def json_parser(input: str):
    """
    takes incomming string and translates it too valid python
    """
    return json.loads(input)