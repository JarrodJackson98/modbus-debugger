#!/usr/bin/env python3
"""
Modbus RTU server on /dev/ttyUSB0
- Unit ID: 1
- Holding register 21 contains 13.7 encoded as a 16-bit integer with 1 decimal place (137)
"""

import logging
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext, ModbusSparseDataBlock
from pymodbus.server import StartSerialServer
from pymodbus.framer import ModbusRtuFramer

# --- config ---
PORT = "/dev/ttyUSB0"
BAUDRATE = 9600
PARITY = "N"          # 'N', 'E', or 'O'
STOPBITS = 1
BYTESIZE = 8
UNIT_ID = 1

# Expose 13.7 as a 16-bit value with 1 decimal place scaling: int(13.7 * 10) = 137
SCALE = 10
FLOAT_VALUE = 13.7
INT16_VALUE = int(round(FLOAT_VALUE * SCALE)) & 0xFFFF
REGISTER_ADDRESS = 21  # zero-based index inside server's datastore

def main():
    logging.basicConfig(level=logging.INFO)
    logging.getLogger("pymodbus").setLevel(logging.INFO)

    # Only map the register(s) we care about
    block = ModbusSparseDataBlock({REGISTER_ADDRESS: INT16_VALUE})

    # HR = holding registers, IR/CO/DI left unused but required by context
    store = ModbusSlaveContext(
        di=ModbusSparseDataBlock({}),
        co=ModbusSparseDataBlock({}),
        hr=block,
        ir=ModbusSparseDataBlock({}),
        zero_mode=True,  # addresses are 0-based; "21" here is exactly HR 21
    )
    context = ModbusServerContext(slaves={UNIT_ID: store}, single=False)

    logging.info(
        f"Starting Modbus RTU server on {PORT} @ {BAUDRATE}{PARITY}{STOPBITS}, "
        f"Unit {UNIT_ID}, HR[{REGISTER_ADDRESS}] = {INT16_VALUE} (scaled from {FLOAT_VALUE})"
    )

    # Run the RTU server
    StartSerialServer(
        context,
        framer=ModbusRtuFramer,
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
