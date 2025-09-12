import serial
import time
import binascii
import argparse

def read_serial(port, baudrate, timeout=1):
    # Open the serial port
    ser = serial.Serial(port, baudrate, timeout=timeout)
    print(f"Opened {ser.name} at {baudrate} baud")

    try:
        while True:
            if ser.in_waiting > 0:
                data = ser.read(ser.in_waiting)  # read all waiting bytes
                if data:
                    print(f"Raw: {data}")
                    print(f"Hex: {binascii.hexlify(data).decode('utf-8')}")
            time.sleep(0.1)

    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        ser.close()
        print("Serial port closed")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Read raw packets from a serial port.")
    parser.add_argument("port", help="Serial port (e.g. COM3, /dev/ttyUSB0)")
    parser.add_argument("baud", type=int, help="Baud rate (e.g. 9600, 115200)")
    args = parser.parse_args()

    read_serial(args.port, args.baud)
