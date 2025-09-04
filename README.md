# Modbus Debugger

A simple Python tool for debugging Modbus RTU communication over serial connections.

## Features

- Send Modbus RTU frames with custom parameters
- Calculate CRC checksums automatically
- Display both transmitted and received data in hex format
- Configurable serial port settings (baud rate, parity, stop bits)
- Support for different Modbus function codes

## Installation

This project uses `uv` for dependency management. Install dependencies with:

```bash
uv sync
```

## Usage

The main script `send_modbus.py` provides a function to send Modbus RTU frames:

```python
from send_modbus import send_modbus

# Read 2 holding registers starting at address 0
send_modbus('/dev/ttyUSB0', 9600, 'N', 1, 1, 3, [0x00, 0x00, 0x00, 0x02])
```

### Parameters

- `dev`: Serial device path (default: '/dev/ttyUSB0')
- `baud`: Baud rate (default: 9600)
- `parity`: Parity setting - 'N' (None), 'E' (Even), 'O' (Odd) (default: 'N')
- `stopbits`: Number of stop bits - 1 or 2 (default: 1)
- `slave`: Modbus slave address (default: 1)
- `func`: Modbus function code (default: 3 for Read Holding Registers)
- `data`: Data bytes for the Modbus frame (default: [0,0,0,2])

## Example

```bash
python send_modbus.py
```

This will send a Modbus RTU frame to read 2 holding registers starting at address 0 from slave device 1, and display both the transmitted and received data in hexadecimal format.

## Requirements

- Python 3.13+
- pymodbus
- pyserial
