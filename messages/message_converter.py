from struct import Struct
from .message_type import MessageType
from .message import Message
from tcc_types import TccCommand, TccParameter, TccTimeout
from logger import setup_logger

class MessageConverter:
    """
    Utility class for converting TCC messages to and from bytes.

    Message format: [type (1), argument (2), value (4), status (1)] = 8 bytes.
    """
    _ONE_BYTE_INT_STRUCT = Struct('>B')      # 1 byte for int (big-endian)
    _TWO_BYTE_INT_STRUCT = Struct('>H')      # 2 bytes for int (big-endian)
    _FOUR_BYTE_FLOAT_STRUCT = Struct('>f')   # 4 bytes for float (big-endian)
    _FOUR_BYTE_INT_STRUCT = Struct('>i')     # 4 bytes for int (big-endian)

    logger = setup_logger("messages")

    @classmethod
    def bytes_to_message(cls, msg: bytes) -> Message:
        """
        Converts a byte string into a Message object.

        Parameters
        ----------
        msg : bytes
            Raw message data (expected length: 8 bytes).

        Returns
        -------
        Message
            Decoded message object. Returns default Message if invalid.
        """
        if len(msg) != 8:
            cls.logger.warning(f"Invalid message length: {len(msg)}, expected 8")
            return Message()

        try:
            type_value = cls._ONE_BYTE_INT_STRUCT.unpack_from(msg, 0)[0]
            msg_type = MessageType(type_value)
        except ValueError:
            cls.logger.warning(f"Unknown message type value: {type_value}")
            return Message()

        arg_id = cls._TWO_BYTE_INT_STRUCT.unpack_from(msg, 1)[0]
        value = cls._FOUR_BYTE_FLOAT_STRUCT.unpack_from(msg, 3)[0]
        status = bool(cls._ONE_BYTE_INT_STRUCT.unpack_from(msg, 7)[0])

        argument = None
        if msg_type == MessageType.COMMAND:
            try:
                argument = TccCommand(arg_id)
            except ValueError:
                cls.logger.warning(f"Invalid command ID: {arg_id}")
                return Message(msg_type, None, None, False)
        elif msg_type in (MessageType.GET_PARAMETER, MessageType.SET_PARAMETER):
            try:
                argument = TccParameter(arg_id)
            except ValueError:
                cls.logger.warning(f"Invalid parameter ID: {arg_id}")
                return Message(msg_type, None, None, False)
        elif msg_type == MessageType.GET_TIMEOUT:
            try:
                argument = TccTimeout(arg_id)
                value = int(value)  # Convert float to int for timeouts
            except ValueError:
                cls.logger.warning(f"Invalid timeout ID: {arg_id}")
                return Message(msg_type, None, None, False)
        elif msg_type == MessageType.CHECK:
            value = None  # CHECK messages don't use value

        cls.logger.debug(f"Decoded message: type={msg_type}, arg={argument}, value={value}, status={status}")
        return Message(msg_type, argument, value, status)

    @classmethod
    def message_to_bytes(cls, msg: Message) -> bytes:
        """
        Converts a Message object into a byte string.

        Parameters
        ----------
        msg : Message
            Message to encode.

        Returns
        -------
        bytes
            Encoded message (8 bytes).
        """
        buffer = bytearray(8)
        type_value = msg.type.value if msg.type else MessageType.UNDEFINED.value
        cls._ONE_BYTE_INT_STRUCT.pack_into(buffer, 0, type_value)

        arg_id = msg.argument.value if msg.argument else 0
        cls._TWO_BYTE_INT_STRUCT.pack_into(buffer, 1, arg_id)

        # Encode value based on message type
        value = msg.value if msg.value is not None else 0.0
        if msg.type in (MessageType.GET_TIMEOUT, MessageType.SET_TIMEOUT):
            cls._FOUR_BYTE_INT_STRUCT.pack_into(buffer, 3, int(value))
        else:
            cls._FOUR_BYTE_FLOAT_STRUCT.pack_into(buffer, 3, float(value))

        status = int(msg.status) if msg.status is not None else 0
        cls._ONE_BYTE_INT_STRUCT.pack_into(buffer, 7, status)

        cls.logger.debug(f"Encoded message: {list(buffer)}")
        return bytes(buffer)

    @staticmethod
    def bytes_to_float(data: bytes) -> float:
        """
        Converts a 4-byte sequence to a float (big-endian).

        Parameters
        ----------
        data : bytes
            4-byte sequence.

        Returns
        -------
        float
            Decoded float value.

        Raises
        ------
        ValueError
            If data length is not 4 bytes.
        """
        if len(data) != 4:
            raise ValueError(f"Expected 4 bytes, got {len(data)}")
        return MessageConverter._FOUR_BYTE_FLOAT_STRUCT.unpack(data)[0]

    @staticmethod
    def bytes_to_int_4(data: bytes) -> int:
        """
        Converts a 4-byte sequence to an int (big-endian).

        Parameters
        ----------
        data : bytes
            4-byte sequence.

        Returns
        -------
        int
            Decoded int value.

        Raises
        ------
        ValueError
            If data length is not 4 bytes.
        """
        if len(data) != 4:
            raise ValueError(f"Expected 4 bytes, got {len(data)}")
        return MessageConverter._FOUR_BYTE_INT_STRUCT.unpack(data)[0]

    @staticmethod
    def float_to_bytes(value: float) -> bytes:
        """
        Converts a float to a 4-byte sequence (big-endian).

        Parameters
        ----------
        value : float
            Float value.

        Returns
        -------
        bytes
            4-byte representation.
        """
        return MessageConverter._FOUR_BYTE_FLOAT_STRUCT.pack(value)

    @staticmethod
    def int_to_bytes(value: int, length: int) -> bytes:
        """
        Converts an integer to a byte sequence (big-endian).

        Parameters
        ----------
        value : int
            Integer value.
        length : int
            Number of bytes.

        Returns
        -------
        bytes
            Byte representation.

        Raises
        ------
        OverflowError
            If value cannot fit in the specified length.
        """
        return value.to_bytes(length, byteorder='big', signed=True)