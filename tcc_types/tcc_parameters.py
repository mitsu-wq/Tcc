"""
Configuration for TCC parameters received from the CAN bus.

Defines parameter types, parameter enumerations, and their configurations including
CAN IDs, data types, and optional dividers for scaled values.
"""
from enum import Enum
from collections import namedtuple

CanParameter = namedtuple('CanParameter', ['can_id', 'type', 'divider'], defaults=[None])

class ProcessType(Enum):
    """
    Types of data processing for CAN message parameters.
    """
    FLOAT = 0        # 32-bit float extracted from bytes 4-7
    INT = 1          # 8-bit integer from byte 4
    BIG_INT = 2      # 32-bit integer from bytes 4-7
    BIG_INT_DIV = 3  # 32-bit integer from bytes 4-7, divided by a scaler
    BOOL = 4         # Boolean value from byte 4

class TccParameter(Enum):
    """
    Enumerates TCC parameters for monitoring hardware states.
    """
    # yaw-response
    YAW_POSITION = 1       # Current yaw angle
    YAW_VELOCITY = 2       # Yaw rotation speed
    YAW_ENGINE = 3         # Yaw engine control
    YAW_MOTION_MODE = 4    # Yaw motion mode
    YAW_POWER = 5          # Yaw power status

    # pitch-response
    PITCH_POSITION = 6     # Current pitch angle
    PITCH_VELOCITY = 7     # Pitch rotation speed
    PITCH_ENGINE = 8       # Pitch engine control
    PITCH_MOTION_MODE = 9  # Pitch motion mode
    PITCH_POWER = 10       # Pitch power status

    # states
    FAN_STATE = 11         # Fan on/off state
    CASE_TEMPERATURE = 12  # Internal case temperature
    COVER_STATE = 13       # Cover open/closed state
    CHARGING_CURRENT = 14  # Battery charging current
    CHARGING_STATE = 15    # Battery charging status
    GLOBAL_SHOT_COUNTER = 16  # Total event counter
    YAW_CURRENT_STATUS = 17   # Yaw mechanism status

    # rover-gnss
    ROV_GNSS_HEADING = 18  # Rover heading from GNSS
    ROV_GNSS_ACCURACY = 19  # Rover GNSS accuracy
    ROV_GNSS_YAW = 20      # Rover yaw angle from GNSS
    
    # base-gnss
    BASE_GNSS_LATITUDE = 21   # Base station latitude
    BASE_GNSS_LONGITUDE = 22  # Base station longitude
    BASE_GNSS_SEA_LEVEL = 23  # Base station altitude
    BASE_GNSS_ACCURACY = 24   # Base station GNSS accuracy

    # global-pos
    GLOBAL_PITCH_POSITION_INCL = 25  # Global pitch inclination
    GLOBAL_ROLL_POSITION_INCL = 26   # Global roll inclination

PARAMETERS_CONFIG = {
    # yaw-response
    TccParameter.YAW_POSITION: CanParameter(
        1303, ProcessType.FLOAT),           # Yaw angle in degrees
    TccParameter.YAW_VELOCITY: CanParameter(
        1304, ProcessType.FLOAT),           # Yaw speed in degrees/sec
    TccParameter.YAW_ENGINE: CanParameter(
        1305, None),                        # Yaw engine (type TBD)
    TccParameter.YAW_MOTION_MODE: CanParameter(
        1308, ProcessType.INT),             # Motion mode: 0=Free, 1=No brakes, 2=Auto
    TccParameter.YAW_POWER: CanParameter(
        1309, None),                        # Yaw power (type TBD)

    # pitch-response
    TccParameter.PITCH_POSITION: CanParameter(
        1313, ProcessType.FLOAT),           # Pitch angle in degrees
    TccParameter.PITCH_VELOCITY: CanParameter(
        1314, ProcessType.FLOAT),           # Pitch speed in degrees/sec
    TccParameter.PITCH_ENGINE: CanParameter(
        1315, None),                        # Pitch engine (type TBD)
    TccParameter.PITCH_MOTION_MODE: CanParameter(
        1318, ProcessType.INT),             # Pitch motion mode
    TccParameter.PITCH_POWER: CanParameter(
        1319, None),                        # Pitch power (type TBD)

    # states
    TccParameter.FAN_STATE: CanParameter(
        1404, ProcessType.BOOL),            # Fan: True=On, False=Off
    TccParameter.CASE_TEMPERATURE: CanParameter(
        1405, ProcessType.FLOAT),           # Temperature in Celsius
    TccParameter.COVER_STATE: CanParameter(
        1409, ProcessType.BOOL),            # Cover: True=Open, False=Closed
    TccParameter.CHARGING_CURRENT: CanParameter(
        1413, ProcessType.FLOAT),           # Charging current in amperes
    TccParameter.CHARGING_STATE: CanParameter(
        1415, ProcessType.BOOL),            # Charging: True=Active, False=Inactive
    TccParameter.GLOBAL_SHOT_COUNTER: CanParameter(
        1418, ProcessType.BIG_INT),         # Total event count
    TccParameter.YAW_CURRENT_STATUS: CanParameter(
        1467, ProcessType.BOOL),            # Yaw status: True=Active, False=Inactive

    # rover-gnss
    TccParameter.ROV_GNSS_HEADING: CanParameter(
        1507, ProcessType.BIG_INT_DIV, 100000.0),  # Heading in degrees
    TccParameter.ROV_GNSS_ACCURACY: CanParameter(
        1509, ProcessType.BIG_INT_DIV, 100000.0),  # Accuracy in meters
    TccParameter.ROV_GNSS_YAW: CanParameter(
        1800, ProcessType.FLOAT),                  # Yaw angle in degrees
    
    # base-gnss
    TccParameter.BASE_GNSS_LATITUDE: CanParameter(
        1520, ProcessType.BIG_INT_DIV, 10000000.0),  # Latitude in degrees
    TccParameter.BASE_GNSS_LONGITUDE: CanParameter(
        1521, ProcessType.BIG_INT_DIV, 10000000.0),  # Longitude in degrees
    TccParameter.BASE_GNSS_SEA_LEVEL: CanParameter(
        1523, ProcessType.BIG_INT_DIV, 1000.0),      # Altitude in meters
    TccParameter.BASE_GNSS_ACCURACY: CanParameter(
        1524, ProcessType.BIG_INT_DIV, 10000.0),     # Accuracy in meters

    # global-pos
    TccParameter.GLOBAL_PITCH_POSITION_INCL: CanParameter(
        1801, ProcessType.FLOAT),                    # Pitch inclination in degrees
    TccParameter.GLOBAL_ROLL_POSITION_INCL: CanParameter(
        1802, ProcessType.FLOAT),                    # Roll inclination in degrees
}

PARAMETERS_DATA = {
    # yaw-response
    TccParameter.YAW_POSITION: 0.0,          # Current yaw angle in degrees (-180.0 to 180.0)
    TccParameter.YAW_VELOCITY: 0.0,          # Current yaw rotation speed in degrees/sec
    TccParameter.YAW_ENGINE: 0.0,            # Yaw engine control value (e.g., torque or power)
    TccParameter.YAW_MOTION_MODE: 0,         # Yaw motion mode: 0=Free run, 1=Without brakes, 2=Auto brakes
    TccParameter.YAW_POWER: 0,               # Yaw power consumption or status (TBD units)
    
    # pitch-response
    TccParameter.PITCH_POSITION: 0.0,        # Current pitch angle in degrees (-20.0 to 90.0)
    TccParameter.PITCH_VELOCITY: 0.0,        # Current pitch rotation speed in degrees/sec
    TccParameter.PITCH_ENGINE: 0.0,          # Pitch engine control value (e.g., torque or power)
    TccParameter.PITCH_MOTION_MODE: 0,       # Pitch motion mode: 0=Free run, 1=Without brakes, 2=Auto brakes
    TccParameter.PITCH_POWER: 0,             # Pitch power consumption or status (TBD units)
    
    # states
    TccParameter.FAN_STATE: False,           # Fan state: True=On, False=Off
    TccParameter.CASE_TEMPERATURE: 0.0,      # Temperature inside the case in degrees Celsius
    TccParameter.COVER_STATE: False,         # Cover state: True=Open, False=Closed
    TccParameter.CHARGING_CURRENT: 0.0,      # Current charging current in amperes
    TccParameter.CHARGING_STATE: False,      # Charging state: True=Charging, False=Not charging
    TccParameter.GLOBAL_SHOT_COUNTER: 0,     # Total number of shots or events recorded
    TccParameter.YAW_CURRENT_STATUS: False,  # Yaw mechanism status: True=Active, False=Inactive
    
    # rover-gnss
    TccParameter.ROV_GNSS_HEADING: 0.0,      # Rover GNSS heading in degrees
    TccParameter.ROV_GNSS_ACCURACY: 0.0,     # Rover GNSS accuracy in meters
    TccParameter.ROV_GNSS_YAW: 0.0,          # Rover GNSS yaw angle in degrees
    
    # base-gnss
    TccParameter.BASE_GNSS_LATITUDE: 0.0,    # Base station latitude in degrees
    TccParameter.BASE_GNSS_LONGITUDE: 0.0,   # Base station longitude in degrees
    TccParameter.BASE_GNSS_SEA_LEVEL: 0.0,   # Base station altitude above sea level in meters
    TccParameter.BASE_GNSS_ACCURACY: 0.0,    # Base station GNSS accuracy in meters
    
    # global-pos
    TccParameter.GLOBAL_PITCH_POSITION_INCL: 0.0,  # Global pitch inclination angle in degrees
    TccParameter.GLOBAL_ROLL_POSITION_INCL: 0.0,   # Global roll inclination angle in degrees
}