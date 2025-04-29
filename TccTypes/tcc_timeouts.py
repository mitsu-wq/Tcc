"""
Configuration for TCC timeouts for CAN bus operations.

Defines timeout types, timeout enumerations, and their configurations including
associated parameters and timeout types (individual or combined).
"""
from enum import Enum
from collections import namedtuple
from .tcc_parameters import TccParameter

CanTimeout = namedtuple('CanTimeout', ['parents', 'type', 'range'], defaults=[None])

class TimeoutType(Enum):
    """
    Types of timeout configurations for TCC parameters.
    """
    COMBINE = 0     # Combined timeout for multiple parameters
    MAIN = 0x01     # Timeout for main system parameters
    ROVER = 0x05    # Timeout for rover GNSS parameters
    BASE = 0x06     # Timeout for base GNSS parameters
    CAMERA = 0x07   # Timeout for camera parameters

class TccTimeout(Enum):
    """
    Enumerates TCC timeouts for monitoring parameter updates.
    """
    # yaw-response
    YAW_RESPONSE = 1        # Combined timeout for yaw-related parameters
    YAW_POSITION = 2        # Yaw angle timeout
    YAW_VELOCITY = 3        # Yaw speed timeout
    YAW_ENGINE = 4          # Yaw engine timeout
    YAW_MOTION_MODE = 5     # Yaw motion mode timeout
    YAW_POWER = 6           # Yaw power timeout

    # pitch-response
    PITCH_RESPONSE = 7     # Combined timeout for pitch-related parameters
    PITCH_POSITION = 8     # Pitch angle timeout
    PITCH_VELOCITY = 9     # Pitch speed timeout
    PITCH_ENGINE = 10       # Pitch engine timeout
    PITCH_MOTION_MODE = 11  # Pitch motion mode timeout
    PITCH_POWER = 12        # Pitch power timeout

    # states
    STATES = 13              # Combined timeout for system states
    FAN_STATE = 14           # Fan state timeout
    CASE_TEMPERATURE = 15    # Case temperature timeout
    CHARGING_CURRENT = 16   # Charging current timeout
    CHARGING_STATE = 17     # Charging state timeout
    GLOBAL_SHOT_COUNTER = 18  # Event counter timeout
    COVER_STATE = 19        # Cover state timeout
    YAW_CURRENT_STATUS = 20  # Yaw status timeout

    # rover-gnss
    ROVER_GNSS = 21         # Combined timeout for rover GNSS data
    ROV_GNSS_HEADING = 22   # Rover heading timeout
    ROV_GNSS_ACCURACY = 23  # Rover accuracy timeout
    ROV_GNSS_YAW = 24       # Rover yaw timeout

    # base-gnss
    BASE_GNSS = 25          # Combined timeout for base GNSS data
    BASE_GNSS_LATITUDE = 26   # Base latitude timeout
    BASE_GNSS_LONGITUDE = 27  # Base longitude timeout
    BASE_GNSS_SEA_LEVEL = 28  # Base altitude timeout
    BASE_GNSS_ACCURACY = 29   # Base accuracy timeout

    # global-pos
    GLOBAL_POS = 30         # Combined timeout for global position data
    GLOBAL_PITCH_POSITION_INCL = 31  # Global pitch inclination timeout
    GLOBAL_ROLL_POSITION_INCL = 32   # Global roll inclination timeout

TIMEOUTS_CONFIG = {
    # yaw-response
    TccTimeout.YAW_RESPONSE: CanTimeout([
        TccTimeout.YAW_POSITION,
        TccTimeout.YAW_VELOCITY,
        TccTimeout.YAW_ENGINE,
        TccTimeout.YAW_MOTION_MODE,
        TccTimeout.YAW_POWER
    ], TimeoutType.COMBINE),  # Groups all yaw-related timeouts
    TccTimeout.YAW_POSITION: CanTimeout(
        TccParameter.YAW_POSITION, TimeoutType.MAIN),  # Timeout for yaw angle
    TccTimeout.YAW_VELOCITY: CanTimeout(
        TccParameter.YAW_VELOCITY, TimeoutType.MAIN),  # Timeout for yaw speed
    TccTimeout.YAW_ENGINE: CanTimeout(
        TccParameter.YAW_ENGINE, TimeoutType.MAIN),    # Timeout for yaw engine
    TccTimeout.YAW_MOTION_MODE: CanTimeout(
        TccParameter.YAW_MOTION_MODE, TimeoutType.MAIN),  # Timeout for yaw mode
    TccTimeout.YAW_POWER: CanTimeout(
        TccParameter.YAW_POWER, TimeoutType.MAIN),     # Timeout for yaw power

    # pitch-response
    TccTimeout.PITCH_RESPONSE: CanTimeout([
        TccTimeout.PITCH_POSITION,
        TccTimeout.PITCH_VELOCITY,
        TccTimeout.PITCH_ENGINE,
        TccTimeout.PITCH_MOTION_MODE,
        TccTimeout.PITCH_POWER,
        TccTimeout.COVER_STATE
    ], TimeoutType.COMBINE),  # Groups all pitch-related timeouts
    TccTimeout.PITCH_POSITION: CanTimeout(
        TccParameter.PITCH_POSITION, TimeoutType.MAIN),  # Timeout for pitch angle
    TccTimeout.PITCH_VELOCITY: CanTimeout(
        TccParameter.PITCH_VELOCITY, TimeoutType.MAIN),  # Timeout for pitch speed
    TccTimeout.PITCH_ENGINE: CanTimeout(
        TccParameter.PITCH_ENGINE, TimeoutType.MAIN),  # Timeout for pitch engine
    TccTimeout.PITCH_MOTION_MODE: CanTimeout(
        TccParameter.PITCH_MOTION_MODE, TimeoutType.MAIN),  # Timeout for pitch mode
    TccTimeout.PITCH_POWER: CanTimeout(
        TccParameter.PITCH_POWER, TimeoutType.MAIN),   # Timeout for pitch power

    # states
    TccTimeout.STATES: CanTimeout([
        TccTimeout.FAN_STATE,
        TccTimeout.CASE_TEMPERATURE,
        TccTimeout.CHARGING_CURRENT,
        TccTimeout.CHARGING_STATE,
        TccTimeout.GLOBAL_SHOT_COUNTER,
        TccTimeout.COVER_STATE,
        TccTimeout.YAW_CURRENT_STATUS
    ], TimeoutType.COMBINE),  # Groups all system state timeouts
    TccTimeout.FAN_STATE: CanTimeout(
        TccParameter.FAN_STATE, TimeoutType.MAIN),     # Timeout for fan state
    TccTimeout.CASE_TEMPERATURE: CanTimeout(
        TccParameter.CASE_TEMPERATURE, TimeoutType.MAIN),  # Timeout for temperature
    TccTimeout.CHARGING_CURRENT: CanTimeout(
        TccParameter.CHARGING_CURRENT, TimeoutType.MAIN),  # Timeout for charging current
    TccTimeout.CHARGING_STATE: CanTimeout(
        TccParameter.CHARGING_STATE, TimeoutType.MAIN),  # Timeout for charging state
    TccTimeout.GLOBAL_SHOT_COUNTER: CanTimeout(
        TccParameter.GLOBAL_SHOT_COUNTER, TimeoutType.MAIN),  # Timeout for event count
    TccTimeout.COVER_STATE: CanTimeout(
        TccParameter.COVER_STATE, TimeoutType.MAIN),   # Timeout for cover state
    TccTimeout.YAW_CURRENT_STATUS: CanTimeout(
        TccParameter.YAW_CURRENT_STATUS, TimeoutType.MAIN),  # Timeout for yaw status

    # rover-gnss
    TccTimeout.ROVER_GNSS: CanTimeout([
        TccTimeout.ROV_GNSS_HEADING,
        TccTimeout.ROV_GNSS_ACCURACY,
        TccTimeout.ROV_GNSS_YAW
    ], TimeoutType.COMBINE),  # Groups all rover GNSS timeouts
    TccTimeout.ROV_GNSS_HEADING: CanTimeout(
        TccParameter.ROV_GNSS_HEADING, TimeoutType.ROVER),  # Timeout for rover heading
    TccTimeout.ROV_GNSS_ACCURACY: CanTimeout(
        TccParameter.ROV_GNSS_ACCURACY, TimeoutType.ROVER),  # Timeout for rover accuracy
    TccTimeout.ROV_GNSS_YAW: CanTimeout(
        TccParameter.ROV_GNSS_YAW, TimeoutType.ROVER),  # Timeout for rover yaw

    # base-gnss
    TccTimeout.BASE_GNSS: CanTimeout([
        TccTimeout.BASE_GNSS_LATITUDE,
        TccTimeout.BASE_GNSS_LONGITUDE,
        TccTimeout.BASE_GNSS_SEA_LEVEL,
        TccTimeout.BASE_GNSS_ACCURACY
    ], TimeoutType.COMBINE),  # Groups all base GNSS timeouts
    TccTimeout.BASE_GNSS_LATITUDE: CanTimeout(
        TccParameter.BASE_GNSS_LATITUDE, TimeoutType.BASE),  # Timeout for base latitude
    TccTimeout.BASE_GNSS_LONGITUDE: CanTimeout(
        TccParameter.BASE_GNSS_LONGITUDE, TimeoutType.BASE),  # Timeout for base longitude
    TccTimeout.BASE_GNSS_SEA_LEVEL: CanTimeout(
        TccParameter.BASE_GNSS_SEA_LEVEL, TimeoutType.BASE),  # Timeout for base altitude
    TccTimeout.BASE_GNSS_ACCURACY: CanTimeout(
        TccParameter.BASE_GNSS_ACCURACY, TimeoutType.BASE),  # Timeout for base accuracy

    # global-pos
    TccTimeout.GLOBAL_POS: CanTimeout([
        TccTimeout.GLOBAL_PITCH_POSITION_INCL,
        TccTimeout.GLOBAL_ROLL_POSITION_INCL
    ], TimeoutType.COMBINE),  # Groups all global position timeouts
    TccTimeout.GLOBAL_PITCH_POSITION_INCL: CanTimeout(
        TccParameter.GLOBAL_PITCH_POSITION_INCL, TimeoutType.MAIN),  # Timeout for pitch inclination
    TccTimeout.GLOBAL_ROLL_POSITION_INCL: CanTimeout(
        TccParameter.GLOBAL_ROLL_POSITION_INCL, TimeoutType.MAIN),  # Timeout for roll inclination
}

TIMEOUTS_DATA = {
    # yaw-response
    TccTimeout.YAW_RESPONSE: 20,          # Combined yaw response timeout in milliseconds
    TccTimeout.YAW_POSITION: 0,           # Yaw position timeout in milliseconds
    TccTimeout.YAW_VELOCITY: 0,           # Yaw velocity timeout in milliseconds
    TccTimeout.YAW_ENGINE: 0,             # Yaw engine timeout in milliseconds
    TccTimeout.YAW_MOTION_MODE: 0,        # Yaw motion mode timeout in milliseconds
    TccTimeout.YAW_POWER: 0,              # Yaw power timeout in milliseconds

    # pitch-response
    TccTimeout.PITCH_RESPONSE: 20,        # Combined pitch response timeout in milliseconds
    TccTimeout.PITCH_POSITION: 0,         # Pitch position timeout in milliseconds
    TccTimeout.PITCH_VELOCITY: 0,         # Pitch velocity timeout in milliseconds
    TccTimeout.PITCH_ENGINE: 0,           # Pitch engine timeout in milliseconds
    TccTimeout.PITCH_MOTION_MODE: 0,      # Pitch motion mode timeout in milliseconds
    TccTimeout.PITCH_POWER: 0,            # Pitch power timeout in milliseconds

    # states
    TccTimeout.STATES: 20,                # Combined system states timeout in milliseconds
    TccTimeout.FAN_STATE: 0,              # Fan state timeout in milliseconds
    TccTimeout.CASE_TEMPERATURE: 0,       # Case temperature timeout in milliseconds
    TccTimeout.CHARGING_CURRENT: 0,       # Charging current timeout in milliseconds
    TccTimeout.CHARGING_STATE: 0,         # Charging state timeout in milliseconds
    TccTimeout.GLOBAL_SHOT_COUNTER: 0,    # Global shot counter timeout in milliseconds
    TccTimeout.COVER_STATE: 0,            # Cover state timeout in milliseconds
    TccTimeout.YAW_CURRENT_STATUS: 0,     # Yaw current status timeout in milliseconds

    # rover-gnss
    TccTimeout.ROVER_GNSS: 20,            # Combined rover GNSS timeout in milliseconds
    TccTimeout.ROV_GNSS_HEADING: 0,       # Rover GNSS heading timeout in milliseconds
    TccTimeout.ROV_GNSS_ACCURACY: 0,      # Rover GNSS accuracy timeout in milliseconds
    TccTimeout.ROV_GNSS_YAW: 0,           # Rover GNSS yaw timeout in milliseconds
    
    # base-gnss
    TccTimeout.BASE_GNSS: 20,             # Combined base GNSS timeout in milliseconds
    TccTimeout.BASE_GNSS_LATITUDE: 0,     # Base GNSS latitude timeout in milliseconds
    TccTimeout.BASE_GNSS_LONGITUDE: 0,    # Base GNSS longitude timeout in milliseconds
    TccTimeout.BASE_GNSS_SEA_LEVEL: 0,    # Base GNSS sea level timeout in milliseconds
    TccTimeout.BASE_GNSS_ACCURACY: 0,     # Base GNSS accuracy timeout in milliseconds
    
    # global-pos
    TccTimeout.GLOBAL_POS: 20,            # Combined global position timeout in milliseconds
    TccTimeout.GLOBAL_PITCH_POSITION_INCL: 0,  # Global pitch inclination timeout in milliseconds
    TccTimeout.GLOBAL_ROLL_POSITION_INCL: 0,   # Global roll inclination timeout in milliseconds
}