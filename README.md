# TCC CAN Interface

A Python library for communicating with a Tactical Control Component (TCC) over a CAN bus interface. This library provides a high-level interface for controlling and monitoring TCC devices through CAN communication.

## Features

- Thread-safe CAN bus communication
- Support for various TCC commands and parameters
- Configurable timeouts for different operations
- Real-time parameter monitoring
- Comprehensive error handling and logging
- Type-safe interfaces using Python type hints

## Requirements

- Python 3.x
- CAN interface hardware (e.g., SocketCAN compatible device)
- Linux system (for SocketCAN support)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/TccCan.git
cd TccCan
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Dependencies

- python-can (4.5.0)
- packaging (24.2)
- typing_extensions (4.13.2)
- wrapt (1.17.2)

## Usage

```python
from TccCan import TccCan

# Initialize the TCC interface
tcc = TccCan()

# Open the CAN interface
tcc.open('can0')  # Replace with your CAN interface name

# Execute commands
tcc.execute_command(TccCommand.YAW_POSITION, 45.0)  # Set yaw position to 45 degrees

# Get parameter values
yaw_position = tcc.get_param(TccParameter.YAW_POSITION)

# Set timeouts
tcc.set_timeout(TccTimeout.YAW_RESPONSE, 1000)  # Set timeout to 1000ms

# Close the interface when done
tcc.close()
```

## Project Structure

- `TccCan.py`: Main library implementation
- `MessageConverter.py`: Utility functions for message conversion
- `TccTypes/`: Type definitions and configurations
- `logging.json`: Logging configuration

## Error Handling

The library includes comprehensive error handling and logging:
- Invalid commands and parameters are rejected
- CAN communication errors are caught and logged
- Thread-safe operations prevent data corruption
- Timeout configurations prevent hanging operations

## Logging

Logging is configured using the `logging.json` file. The library uses Python's built-in logging system to provide detailed information about:
- CAN message transmission and reception
- Command execution status
- Parameter updates
- Error conditions

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.