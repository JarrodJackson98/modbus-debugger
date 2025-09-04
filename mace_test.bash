#!/bin/bash

# Bash script to read holding register 21 from slave 1 via Modbus RTU

# Adjust these if needed
PORT="/dev/ttyAMA0"
BAUD=9600
SLAVE=1
FUNC=3
ADDR=21
QTY=1

# Run the command using uv
uv run python send_modbus.py \
    --port "$PORT" \
    --baud "$BAUD" \
    --slave "$SLAVE" \
    --func "$FUNC" \
    --addr "$ADDR" \
    --qty "$QTY"
