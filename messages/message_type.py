from enum import Enum

class MessageType(Enum):
    """
    Message types for TCC client-server communication.
    """
    CHECK = 0x00           # Check connection status (returns bool)
    COMMAND = 0x01         # Execute a command (with float/int argument)
    GET_PARAMETER = 0x02   # Retrieve a parameter value (returns float/int/bool)
    GET_TIMEOUT = 0x03     # Retrieve a timeout value (returns int)
    UNDEFINED = 0xFF       # Invalid or unknown message