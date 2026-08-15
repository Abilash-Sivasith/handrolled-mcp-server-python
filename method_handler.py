import json

def init(request):
    pass


def list_tools():
    with open('tools.json', 'r') as file:
        data = json.load(file) 
    return data

def tools_calls_router():
    pass
