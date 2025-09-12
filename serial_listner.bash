#!/bin/bash

# Bash script to read holding register 21 from slave 1 via Modbus RTU

# Adjust these if needed
PORT="/dev/ttyAMA0"
BAUD=9600


# Run the command using uv
uv run python serial_reader.py \
    --port "$PORT" \
    --baud "$BAUD" 
