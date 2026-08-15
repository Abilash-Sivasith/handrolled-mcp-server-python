from abc import ABC, abstractmethod

class Transport(ABC):
    """
    Defines the interface that other transports like stdio, http should follow
    
    """

    @abstractmethod
    def recieve(self) -> str | None:
        """
        recieves msgs from the MCP client
        """
        pass

    @abstractmethod
    def send(self, input: str) -> None:
        """
        sends msg back to the mcp client
        """
        pass