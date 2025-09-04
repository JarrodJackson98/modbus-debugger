import serial, time, logging, argparse

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def modbus_crc(b):
    crc = 0xFFFF
    for x in b:
        crc ^= x
        for _ in range(8):
            crc = (crc >> 1) ^ 0xA001 if (crc & 1) else (crc >> 1)
    return crc & 0xFFFF

def send_modbus(dev='/dev/ttyUSB0', baud=9600, parity='N', stopbits=1, slave=1, func=3, addr=0, qty=2):
    # Convert addr and qty to bytes for the Modbus frame
    data = [(addr >> 8) & 0xFF, addr & 0xFF, (qty >> 8) & 0xFF, qty & 0xFF]
    logger.info(f"Sending Modbus frame to {dev} with baudrate {baud}, parity {parity}, stopbits {stopbits}, slave {slave}, func {func}, addr {addr}, qty {qty}")
    frame_wo = bytes([slave, func] + data)
    crc = modbus_crc(frame_wo)
    frame = frame_wo + bytes([crc & 0xFF, (crc >> 8) & 0xFF])
    ser = serial.Serial(dev, baudrate=baud, bytesize=8,
                        parity={'N':serial.PARITY_NONE,'E':serial.PARITY_EVEN,'O':serial.PARITY_ODD}[parity],
                        stopbits={1:serial.STOPBITS_ONE,2:serial.STOPBITS_TWO}[stopbits],
                        timeout=1)
    ser.write(frame)
    time.sleep(0.1)
    resp = ser.read(256)  # adjust as needed
    ser.close()
    logger.info(f"TX: {frame.hex(' ').upper()}")
    logger.info(f"RX raw: {resp}")
    logger.info(f"RX: {resp.hex(' ').upper()}")

def main():
    parser = argparse.ArgumentParser(description='Send Modbus RTU commands')
    parser.add_argument('--port', default='/dev/ttyUSB0', help='Serial port (default: /dev/ttyUSB0)')
    parser.add_argument('--baud', type=int, default=9600, help='Baud rate (default: 9600)')
    parser.add_argument('--parity', default='N', choices=['N', 'E', 'O'], help='Parity (default: N)')
    parser.add_argument('--stopbits', type=int, default=1, choices=[1, 2], help='Stop bits (default: 1)')
    parser.add_argument('--slave', type=int, default=1, help='Slave ID (default: 1)')
    parser.add_argument('--func', type=int, default=3, help='Function code (default: 3)')
    parser.add_argument('--addr', type=int, default=0, help='Register address (default: 0)')
    parser.add_argument('--qty', type=int, default=2, help='Quantity of registers (default: 2)')
    
    args = parser.parse_args()
    
    send_modbus(
        dev=args.port,
        baud=args.baud,
        parity=args.parity,
        stopbits=args.stopbits,
        slave=args.slave,
        func=args.func,
        addr=args.addr,
        qty=args.qty
    )

if __name__ == "__main__":
    main()
