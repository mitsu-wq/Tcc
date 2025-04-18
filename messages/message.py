from typing import Union, Optional
from .message_type import MessageType
from types import TccCommand, TccParameter, TccTimeout

class Message:
    """
    Represents a TCC message for client-server communication.

    Attributes
    ----------
    type : MessageType
        Type of the message (e.g., COMMAND, GET_PARAMETER).
    argument : TccCommand or TccParameter or TccTimeout or None
        Command, parameter, or timeout identifier.
    value : float or int or bool or None
        Value associated with the message (e.g., command argument, parameter value).
    status : bool or None
        Status of the message (True for success, False for error).
    """
    def __init__(self,
                 type: MessageType = MessageType.UNDEFINED,
                 argument: Optional[Union[TccCommand, TccParameter, TccTimeout]] = None,
                 value: Optional[Union[float, int, bool]] = None,
                 status: Optional[bool] = None):
        self.type = type
        self.argument = argument
        self.value = value
        self.status = status

    def __repr__(self) -> str:
        return (f"Message(type={self.type}, argument={self.argument}, "
                f"value={self.value}, status={self.status})")