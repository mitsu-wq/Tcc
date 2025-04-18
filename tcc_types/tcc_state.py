"""
Defines the state enumeration for the TCC interface.

Provides a clear representation of whether the CAN interface is open or closed.
"""
from enum import Enum

class TccState(Enum):
    """
    States of the TCC CAN interface.
    """
    OPEN = 1   # Interface is active and communicating
    CLOSE = 2  # Interface is inactive or closed