from struct import Struct

class MessageConverter:
    """
    Utility class for converting TCC messages to and from bytes.
    """
    _ONE_BYTE_INT_STRUCT = Struct('>B')      # 1 byte for int (big-endian)
    _TWO_BYTE_INT_STRUCT = Struct('>H')      # 2 bytes for int (big-endian)
    _FOUR_BYTE_FLOAT_STRUCT = Struct('>f')   # 4 bytes for float (big-endian)
    _FOUR_BYTE_INT_STRUCT = Struct('>i')     # 4 bytes for int (big-endian)

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