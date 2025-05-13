import can
import threading
from typing import Union
from .TccTypes import *
from .MessageConverter import MessageConverter
from logging import getLogger, DEBUG, INFO

class TccCan:
    """
    Manages communication with a Tactical Control Component (TCC) over a CAN bus.

    Provides methods to open/close the CAN interface, execute commands, retrieve/set parameters
    and timeouts, and process incoming CAN messages. Maintains thread-safe access to status data.
    """
    def __init__(self):
        """
        Initializes the Tcc instance with default attributes.

        Sets up the CAN bus interface, threading components, and a mutex for thread-safe
        access to shared data structures like PARAMETERS_DATA and TIMEOUTS_DATA.
        """
        self.bus = None
        self.state: TccState = TccState.CLOSE  # Initial state of the CAN interface
        self.stop_thread_flag = threading.Event()  # Flag to signal thread termination
        self.can_thread = None  # Thread for reading CAN messages
        self.status_mutex = threading.Lock()  # Mutex for thread-safe data access
        self.logger = getLogger("TccCan")  # Logger for TCC operations
        self.logger.setLevel(INFO)

    def open(self, interface):
        """
        Opens the CAN interface for communication.

        Initializes the CAN bus, starts a reading thread, and configures initial timeouts.

        Parameters
        ----------
        interface : str
            The CAN interface identifier (e.g., 'can0').

        Returns
        -------
        bool
            True if the interface was opened successfully, False otherwise.
        """
        if self.state == TccState.OPEN:
            self.logger.error(f"CAN interface {interface} is already open")
            return True

        try:
            self.state = TccState.OPEN
            self.bus = can.ThreadSafeBus(channel=interface, interface='socketcan')
            self.stop_thread_flag.clear()
            self.can_thread = threading.Thread(target=self.can_read_thread)
            self.can_thread.start()

            if not self.startup_timeouts():
                raise RuntimeError("Failed to configure initial timeouts")

            self.logger.info(f"CAN interface {interface} opened successfully")
            return True
        except AttributeError:
            self.logger.error("Unsupported 'can.Bus'. Check 'python-can' version.")
            self.close()
            return False
        except Exception as e:
            self.logger.error(f"Failed to open CAN interface {interface}: {e}")
            self.close()
            return False

    def close(self):
        """
        Closes the CAN interface and cleans up resources.

        Stops the reading thread, shuts down the CAN bus, and resets timeouts.

        Returns
        -------
        bool
            True if the interface was closed successfully, False otherwise.
        """
        if self.state != TccState.OPEN:
            self.logger.error("CAN interface is already closed or was never opened")
            return True
        
        try:
            self.state = TccState.CLOSE
            if not self.startup_timeouts():
                self.logger.warning("Failed to reset timeouts during interface closure")
            
            self.stop_thread_flag.set()

            if self.can_thread and self.can_thread.is_alive():
                self.can_thread.join(timeout=1.0)
                if self.can_thread.is_alive():
                    self.logger.warning("CAN read thread did not terminate within 1 second")
            
            if self.bus:
                self.bus.shutdown()

            self.bus = None
            self.can_thread = None
            self.stop_thread_flag.clear()

            self.logger.info("CAN interface closed successfully")
            return True
        except Exception as e:
            self.logger.error(f"Failed to close CAN interface: {e}")
            self.state = TccState.CLOSE
            self.bus = None
            self.can_thread = None
            return False

    def startup_timeouts(self):
        """
        Configures initial timeouts based on the CAN interface state.

        Sets or resets timeouts (e.g., YAW_RESPONSE) depending on whether the interface
        is being opened or closed.

        Returns
        -------
        bool
            True if timeouts were configured successfully, False otherwise.
        """
        try:
            if self.state == TccState.OPEN:
                yaw_value = TIMEOUTS_DATA[TccTimeout.YAW_RESPONSE]
                pitch_value = TIMEOUTS_DATA[TccTimeout.PITCH_RESPONSE]
                states_value = TIMEOUTS_DATA[TccTimeout.STATES]
                rover_gnss_value = TIMEOUTS_DATA[TccTimeout.ROVER_GNSS]
                base_gnss_value = TIMEOUTS_DATA[TccTimeout.BASE_GNSS]
                global_pos_value = TIMEOUTS_DATA[TccTimeout.GLOBAL_POS]
                if not self.set_timeout(TccTimeout.YAW_RESPONSE, yaw_value):
                    self.logger.error("Failed to set YAW_RESPONSE timeout")
                    return False
                if not self.set_timeout(TccTimeout.PITCH_RESPONSE, pitch_value):
                    self.logger.error("Failed to set PITHC_RESPONSE timeout")
                    return False
                if not self.set_timeout(TccTimeout.STATES, states_value):
                    self.logger.error("Failed to set STATES timeout")
                    return False
                if not self.set_timeout(TccTimeout.ROVER_GNSS, rover_gnss_value):
                    self.logger.error("Failed to set ROVER_GNSS timeout")
                    return False
                if not self.set_timeout(TccTimeout.BASE_GNSS, base_gnss_value):
                    self.logger.error("Failed to set BASE_GNSS timeout")
                    return False
                if not self.set_timeout(TccTimeout.GLOBAL_POS, global_pos_value):
                    self.logger.error("Failed to set GLOBAL_POS timeout")
                    return False
            elif self.state == TccState.CLOSE:
                if not self.set_timeout(TccTimeout.YAW_RESPONSE, 0):
                    self.logger.error("Failed to set YAW_RESPONSE timeout")
                    return False
                if not self.set_timeout(TccTimeout.PITCH_RESPONSE, 0):
                    self.logger.error("Failed to set PITHC_RESPONSE timeout")
                    return False
                if not self.set_timeout(TccTimeout.STATES, 0):
                    self.logger.error("Failed to set STATES timeout")
                    return False
                if not self.set_timeout(TccTimeout.ROVER_GNSS, 0):
                    self.logger.error("Failed to set ROVER_GNSS timeout")
                    return False
                if not self.set_timeout(TccTimeout.BASE_GNSS, 0):
                    self.logger.error("Failed to set BASE_GNSS timeout")
                    return False
                if not self.set_timeout(TccTimeout.GLOBAL_POS, 0):
                    self.logger.error("Failed to set GLOBAL_POS timeout")
                    return False
            return True
        except Exception as ex:
            self.logger.error(f"Error configuring timeouts: {ex}")
            return False

    def execute_command(self, command: TccCommand, argument=None) -> bool:
        """
        Executes a TCC command on the hardware via the CAN bus.

        Formats the command data based on its type (SIMPLE or WITH_VALUE) and sends it.

        Parameters
        ----------
        command : TccCommand
            The command to execute (e.g., YAW_POSITION, CONTROL_FAN).
        argument : float or int or None, optional
            The value associated with the command (e.g., angle in degrees). Default is None.

        Returns
        -------
        bool
            True if the command was sent successfully, False if invalid or out of range.
        """
        if command not in COMMANDS_CONFIG:
            self.logger.error(f"Command not implemented: {command}")
            return False
        
        config = COMMANDS_CONFIG[command]
        data = [0] * 8  # Initialize 8-byte CAN message data

        minv, maxv = config.range
        if argument is not None and not minv <= argument <= maxv:
            self.logger.error(f"{command} value {argument} out of range ({minv}, {maxv})")
            return False
        
        data[1] = config.type.value
        if config.type == CommandType.SIMPLE:
            data[4] = argument if argument is not None else 0
        elif config.type == CommandType.WITH_VALUE:
            data[4:8] = MessageConverter.float_to_bytes(argument)

        self.logger.info(f"Executing {command} with value {argument}")
        return self.send_data(config.can_id, data)

    def get_param(self, param: TccParameter) -> Union[float, int, bool, None]:
        """
        Retrieves the current value of a TCC parameter.

        Accesses PARAMETERS_DATA in a thread-safe manner and logs the retrieved value.

        Parameters
        ----------
        param : TccParameter
            The parameter to retrieve (e.g., YAW_POSITION, FAN_STATE).

        Returns
        -------
        float or int or bool or None
            The parameter's value, or None if the parameter is not found.
        """
        with self.status_mutex:
            try:
                value = PARAMETERS_DATA[param]
                self.logger.info(f"Retrieved {param} with value: {value}")
                return value
            except KeyError:
                self.logger.warning(f"Parameter {param} not found in PARAMETERS_DATA")
                return None
    
    def get_timeout(self, timeout: TccTimeout) -> Union[int, None]:
        """
        Retrieves the current value of a TCC timeout.

        Accesses TIMEOUTS_DATA in a thread-safe manner and logs the retrieved value.

        Parameters
        ----------
        timeout : TccTimeout
            The timeout to retrieve (e.g., YAW_RESPONSE, YAW_POSITION).

        Returns
        -------
        int or None
            The timeout value in milliseconds, or None if the timeout is not found.
        """
        with self.status_mutex:
            try:
                value = TIMEOUTS_DATA[timeout]
                self.logger.info(f"Retrieved timeout {timeout} with value: {value} ms")
                return value
            except KeyError:
                self.logger.warning(f"Timeout {timeout} not found in TIMEOUTS_DATA")
                return None

    def set_timeout(self, timeout: TccTimeout, value=None) -> bool:
        """
        Sets a timeout parameter on the CAN bus.

        For combined timeouts, propagates the value to all associated parameters.

        Parameters
        ----------
        timeout : TccTimeout
            The timeout to set (e.g., YAW_RESPONSE, YAW_POSITION).
        value : int, optional
            The timeout value in milliseconds. Must be non-negative.

        Returns
        -------
        bool
            True if the timeout was set successfully, False otherwise.
        """
        if timeout not in TIMEOUTS_CONFIG or value is None or value < 0:
            self.logger.debug(f"Invalid timeout {timeout} or value {value}")
            return False
        
        config = TIMEOUTS_CONFIG[timeout]

        if config.range and not (config.range[0] <= value <= config.range[1]):
            self.logger.debug(f"Value {value} out of range {config.range} for {timeout}")
            return False
        
        if config.type == TimeoutType.COMBINE:
            success = True
            for parent in config.parents:
                if not self.set_timeout(parent, value):
                    success = False
            return success
        
        if config.type not in TimeoutType:
            self.logger.error(f"Unsupported timeout type {config.type} for {timeout}")
            return False

        parent = config.parents
        if not isinstance(parent, TccParameter) or parent not in PARAMETERS_CONFIG:
            self.logger.debug(f"Invalid parent {parent} for {timeout}")
            return False
        
        data = bytearray(8)  # Prepare 8-byte CAN message
        data[0] = config.type.value
        data[1] = 0x0C  # Command identifier for timeout setting
        data[2] = 0x05  # Sub-command for timeout
        data[4:6] = MessageConverter.int_to_bytes(PARAMETERS_CONFIG[parent].can_id, 2)
        data[6:8] = MessageConverter.int_to_bytes(value, 2)

        result = self.send_data(2000, data)
        self.logger.info(f"Set timeout {timeout} to {value} ms: {'Success' if result else 'Failed'}")
        if result:
            with self.status_mutex:
                TIMEOUTS_DATA[timeout] = value
        return result

    def send_data(self, can_id: int, data: list) -> bool:
        """
        Sends a message to the CAN bus.

        Parameters
        ----------
        can_id : int
            The CAN arbitration ID for the message.
        data : list
            A list of 8 bytes to send.

        Returns
        -------
        bool
            True if the message was sent successfully, False otherwise.
        """
        try:
            msg = can.Message(arbitration_id=can_id, data=data, is_extended_id=False)
            self.bus.send(msg)
            self.logger.debug(f"Sent CAN message with ID {can_id}: {data}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to send CAN message: {e}")
            return False

    def can_read_thread(self):
        """
        Continuously reads messages from the CAN bus in a separate thread.

        Processes incoming messages until the stop_thread_flag is set.
        """
        while not self.stop_thread_flag.is_set():
            try:
                msg = self.bus.recv(timeout=1)
                if msg:
                    self.process_can_message(msg)
            except Exception as e:
                self.logger.error(f"Error in CAN read thread: {e}")

    def process_can_message(self, msg: can.Message):
        """
        Processes an incoming CAN message and updates parameters.

        Interprets the message based on its arbitration ID and updates PARAMETERS_DATA.

        Parameters
        ----------
        msg : can.Message
            The received CAN message containing arbitration ID and data.
        """
        can_id_to_param = {config.can_id: param for param, config in PARAMETERS_CONFIG.items()}
        
        with self.status_mutex:
            can_id = msg.arbitration_id
            if can_id not in can_id_to_param:
                self.logger.debug(f"Ignored CAN message with unknown ID: {can_id}")
                return
            
            param = can_id_to_param[can_id]
            config = PARAMETERS_CONFIG[param]

            if config.type == None:
                return
            elif config.type == ProcessType.FLOAT:
                value = MessageConverter.bytes_to_float(msg.data[4:8])
            elif config.type == ProcessType.INT:
                value = msg.data[4]
            elif config.type == ProcessType.BIG_INT:
                value = MessageConverter.bytes_to_int_4(msg.data[4:8])
            elif config.type == ProcessType.BIG_INT_DIV:
                value = MessageConverter.bytes_to_int_4(msg.data[4:8]) / config.divider
            elif config.type == ProcessType.BOOL:
                value = bool(msg.data[4])
            else:
                self.logger.error(f"Unsupported process type {config.type} for {param}")
                return

            current_value = PARAMETERS_DATA[param]
            if current_value != value:
                PARAMETERS_DATA[param] = value
                self.logger.debug(f"Updated {param} (CAN ID {can_id}) to {value}")