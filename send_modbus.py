import serial, time

def modbus_crc(b):
    crc = 0xFFFF
    for x in b:
        crc ^= x
        for _ in range(8):
            crc = (crc >> 1) ^ 0xA001 if (crc & 1) else (crc >> 1)
    return crc & 0xFFFF

def send_modbus(dev='/dev/ttyUSB0', baud=9600, parity='N', stopbits=1, slave=1, func=3, data=[0,0,0,2]):
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
    print("TX:", frame.hex(' ').upper())
    print("RX:", resp.hex(' ').upper())

# Example:
# send_modbus('/dev/ttyUSB0', 9600, 'N', 1, 1, 3, [0x00,0x00, 0x00,0x02])



def main():
    send_modbus('/dev/ttyUSB0', 9600, 'N', 1, 1, 3, [0x00,0x00, 0x00,0x02])


if __name__ == "__main__":
    main()
