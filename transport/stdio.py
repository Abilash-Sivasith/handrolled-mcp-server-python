from .transport import Transport
import sys

class StdioTransport(Transport):

    def recieve(self):
        line : str = sys.stdin.readline()
        if line == None:
            return None
        else:
            return line.strip()

    def send(self, message):
        print(message, flush=None) # flush param tells to print it out to the client immediatly and do not hold in the buffer for efficeny

