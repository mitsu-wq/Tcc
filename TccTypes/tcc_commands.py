"""
Configuration for TCC commands sent over the CAN bus.

Defines command types, command enumerations, and their configurations including
CAN IDs, data types, and valid value ranges.
"""
from enum import Enum
from collections import namedtuple

CanCommand = namedtuple('CanCommand', ['can_id', 'type', 'range'])

class CommandType(Enum):
    """
    Types of TCC commands for data formatting.
    """
    WITH_VALUE = 0x02  # Commands requiring a float value (e.g., angles, speeds)
    SIMPLE = 0x0A      # Commands with a single integer value (e.g., on/off)

class TccCommand(Enum):
    """
    Enumerates available TCC commands for controlling hardware components.
    """
    YAW_POSITION = 1           # Set absolute yaw angle
    YAW_VELOCITY = 2           # Set yaw rotation speed
    YAW_RELATIVE_POSITION = 3  # Set yaw angle relative to current position
    YAW_MOTION_MODE = 4        # Set yaw motion mode (free run, no brakes, auto brakes)
    PITCH_POSITION = 5         # Set absolute pitch angle
    PITCH_VELOCITY = 6         # Set pitch rotation speed
    PITCH_RELATIVE_POSITION = 7  # Set pitch angle relative to current position
    PITCH_MOTION_MODE = 8      # Set pitch motion mode
    CONTROL_COVER = 9          # Open or close the cover
    CONTROL_FAN = 10           # Turn fan on or off
    CONTROL_CHARGE_BATTERY = 11  # Enable or disable battery charging
    CONTROL_OES_HEATER = 12    # Control OES heater
    CONTROL_DRIVES_HEATER = 13  # Control drives heater
    YAW_MIN_POSITION = 14      # Set minimum yaw position limit
    YAW_MAX_POSITION = 15      # Set maximum yaw position limit
    PITCH_MIN_POSITION = 16    # Set minimum pitch position limit
    PITCH_MAX_POSITION = 17    # Set maximum pitch position limit

COMMANDS_CONFIG = {
    TccCommand.YAW_POSITION: CanCommand(
        1300, CommandType.WITH_VALUE, (-180.0, 180.0)),  # Yaw angle in degrees
    TccCommand.YAW_VELOCITY: CanCommand(
        1301, CommandType.WITH_VALUE, (-80.0, 80.0)),    # Yaw speed in degrees/sec
    TccCommand.YAW_RELATIVE_POSITION: CanCommand(
        1302, CommandType.WITH_VALUE, (-180.0, 180.0)),  # Relative yaw angle
    TccCommand.YAW_MOTION_MODE: CanCommand(
        1307, CommandType.SIMPLE, (0, 2)),               # Motion mode: 0=Free, 1=No brakes, 2=Auto
    TccCommand.PITCH_POSITION: CanCommand(
        1310, CommandType.WITH_VALUE, (-20.0, 90.0)),    # Pitch angle in degrees
    TccCommand.PITCH_VELOCITY: CanCommand(
        1311, CommandType.WITH_VALUE, (-80.0, 80.0)),    # Pitch speed in degrees/sec
    TccCommand.PITCH_RELATIVE_POSITION: CanCommand(
        1312, CommandType.WITH_VALUE, (-20.0, 90.0)),    # Relative pitch angle
    TccCommand.PITCH_MOTION_MODE: CanCommand(
        1317, CommandType.SIMPLE, (0, 2)),               # Pitch motion mode
    TccCommand.CONTROL_COVER: CanCommand(
        1400, CommandType.SIMPLE, (0, 1)),               # Cover: 0=Close, 1=Open
    TccCommand.CONTROL_FAN: CanCommand(
        1403, CommandType.SIMPLE, (0, 1)),               # Fan: 0=Off, 1=On
    TccCommand.CONTROL_CHARGE_BATTERY: CanCommand(
        1414, CommandType.SIMPLE, (0, 1)),               # Charging: 0=Off, 1=On
    TccCommand.CONTROL_OES_HEATER: CanCommand(
        1430, CommandType.SIMPLE, (0, 1)),               # OES heater: 0=Off, 1=On
    TccCommand.CONTROL_DRIVES_HEATER: CanCommand(
        1432, CommandType.SIMPLE, (0, 1)),               # Drives heater: 0=Off, 1=On (TBD)
    TccCommand.YAW_MIN_POSITION: CanCommand(
        1653, CommandType.WITH_VALUE, (-180.0, 180.0)),  # Min yaw limit (TBD)
    TccCommand.YAW_MAX_POSITION: CanCommand(
        1655, CommandType.WITH_VALUE, (-180.0, 180.0)),  # Max yaw limit (TBD)
    TccCommand.PITCH_MIN_POSITION: CanCommand(
        1703, CommandType.WITH_VALUE, (-20.0, 90.0)),    # Min pitch limit (TBD)
    TccCommand.PITCH_MAX_POSITION: CanCommand(
        1705, CommandType.WITH_VALUE, (-20.0, 90.0))     # Max pitch limit (TBD)
}