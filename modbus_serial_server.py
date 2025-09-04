#!/usr/bin/env python3
"""
Modbus RTU server on /dev/ttyUSB0
- Unit ID: 1
- Holding register 21 serves 13.7 as a 16-bit int with 1 decimal (137)
- pymodbus >= 3.10 API (Device/ServerContext)
"""

import logging
from pymodbus.datastore import (
    ModbusSparseDataBlock,
    ModbusDeviceContext,
    ModbusServerContext,
)
from pymodbus.server import StartSerialServer

# --- config ---
PORT = "/dev/ttyUSB0"
BAUDRATE = 9600
PARITY = "N"      # 'N','E','O'
STOPBITS = 1
BYTESIZE = 8
UNIT_ID = 1

# 13.7 -> 137 (1 decimal)
SCALE = 10
FLOAT_VALUE = 13.7
INT16_VALUE = int(round(FLOAT_VALUE * SCALE)) & 0xFFFF
REGISTER_ADDRESS = 21  # datastore index

def main():
    logging.basicConfig(level=logging.INFO)
    logging.getLogger("pymodbus").setLevel(logging.INFO)

    # Expose only HR[21] = 137
    hr_block = ModbusSparseDataBlock({REGISTER_ADDRESS: INT16_VALUE})

    # Build device (DI/CO/IR empty, HR populated)
    device = ModbusDeviceContext(
        di=ModbusSparseDataBlock({}),
        co=ModbusSparseDataBlock({}),
        ir=ModbusSparseDataBlock({}),
        hr=hr_block,
    )

    # Map device-id -> context (use positional arg 'devices')
    context = ModbusServerContext({UNIT_ID: device}, single=False)

    logging.info(
        f"RTU server on {PORT} {BAUDRATE}{PARITY}{STOPBITS}, unit {UNIT_ID}, "
        f"HR[{REGISTER_ADDRESS}]={INT16_VALUE} (from {FLOAT_VALUE})"
    )

    # Framer defaults to RTU for serial; no need to specify explicitly in 3.x
    StartSerialServer(
        context=context,
        port=PORT,
        baudrate=BAUDRATE,
        parity=PARITY,
        stopbits=STOPBITS,
        bytesize=BYTESIZE,
        timeout=1,
        reconnect=True,
    )

if __name__ == "__main__":
    main()
