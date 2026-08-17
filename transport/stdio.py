from .transport import Transport
import json
import sys

class StdioTransport(Transport):

    def recieve(self):
        line : str = sys.stdin.readline()
        if line == "": # readline() returns "" at EOF, "\n" for a blank line
            return None
        else:
            return line.strip()

    def send(self, message):
        print(json.dumps(message), flush=True) # flush so the client on the other end of the pipe gets it immediately instead of it sitting in the buffer

