# TCC CAN Interface

This project provides a Python-based interface for communicating with a **Tactical Control Component (TCC)** over a **CAN bus**. It enables control of hardware components, retrieval of system parameters, and configuration of timeouts for various TCC operations. The system is designed to be thread-safe, robust, and extensible, with comprehensive logging for debugging and monitoring.

## Features

- **CAN Bus Communication**: Interfaces with a TCC using the `python-can` library over a SocketCAN interface (e.g., `can0`).
- **Command Execution**: Supports sending commands to control hardware, such as yaw/pitch positioning, fan control, and battery charging.
- **Parameter Retrieval**: Retrieves real-time hardware states, including yaw/pitch angles, GNSS data, and system statuses.
- **Timeout Configuration**: Configures and monitors timeouts for system parameters to ensure timely updates.
- **Thread-Safe Design**: Uses mutex locks to ensure safe access to shared data structures.
- **Logging**: Implements detailed logging with file rotation for debugging and operational monitoring.

## Project Structure

The project is organized into several key modules:

- `tcc.py`: Core class (`Tcc`) for managing CAN bus communication, including opening/closing the interface, sending commands, and processing incoming messages.
- `tcc_timeouts.py`: Defines timeout configurations and enumerations for monitoring parameter updates.
- `tcc_state.py`: Enumerates the states of the CAN interface (OPEN or CLOSE).
- `tcc_parameters.py`: Configures parameters received from the CAN bus, including data types and CAN IDs.
- `tcc_commands.py`: Defines commands for controlling hardware, including CAN IDs and value ranges.
- `message_type.py`: Enumerates message types for client-server communication.
- `message_converter.py`: Utility for converting messages to/from bytes for CAN communication.
- `message.py`: Defines the `Message` class for structured communication.
- `logger.py`: Configures logging with file rotation for debugging and monitoring.

## Requirements

The project requires Python 3.6+ and the following dependencies, listed in `requirements.txt`:

```
packaging==24.2
python-can==4.5.0
typing_extensions==4.13.2
wrapt==1.17.2
```

## Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/mitsu-wq/Tcc.git
   cd Tcc
   ```

2. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure CAN Interface**: Ensure a CAN interface (e.g., `can0`) is available and configured on your system. For Linux, you may need to set up SocketCAN:

   ```bash
   sudo modprobe can
   sudo modprobe vcan
   sudo ip link add dev can0 type vcan
   sudo ip link set up can0
   ```

## Usage

The `Tcc` class provides the primary interface for interacting with the TCC hardware. Below is an example of how to use it:

```python
from tcc import Tcc
from tcc_types import TccCommand, TccParameter

# Initialize TCC
tcc = Tcc()

# Open CAN interface
if tcc.open("can0"):
    print("CAN interface opened successfully")
else:
    print("Failed to open CAN interface")
    exit(1)

# Execute a command (e.g., set yaw position to 45 degrees)
tcc.execute_command(TccCommand.YAW_POSITION, 45.0)

# Retrieve a parameter (e.g., current yaw position)
yaw_position = tcc.get_param(TccParameter.YAW_POSITION)
print(f"Current yaw position: {yaw_position} degrees")

# Set a timeout (e.g., yaw response timeout to 50 ms)
tcc.set_timeout(TccTimeout.YAW_RESPONSE, 50)

# Close CAN interface
tcc.close()
```