import serial
import csv
import time
from datetime import datetime
import os

SERIAL_PORT = "COM8"  # Change this to your actual port
BAUD_RATE = 115200
CSV_FILE = "Serial_data.csv"

def main():
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        print(f"Connected to {SERIAL_PORT} at {BAUD_RATE} baud.")

        with open(CSV_FILE, mode="a", newline="") as file:
            writer = csv.writer(file)

            # Only write header once
            if os.stat(CSV_FILE).st_size == 0:
                writer.writerow(["Timestamp", "Serial Data"])

            while True:
                try:
                    # Read and decode line from serial
                    line_raw = ser.readline().decode("utf-8", errors="ignore").strip()
                    if not line_raw:
                        continue

                    print(f"Raw Data: {line_raw}")

                    # Convert to list of integers
                    data_values = [int(x) for x in line_raw.split(',') if x.strip().isdigit()]

                    # Save to CSV
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    writer.writerow([timestamp, ','.join(map(str, data_values))])
                    file.flush()
                    print(f"Data saved at {timestamp}")

                except KeyboardInterrupt:
                    print("\nUser stopped the script.")
                    break
                except Exception as e:
                    print(f"Error processing data: {e}")

    except Exception as e:
        print(f"Serial connection failed: {e}")
        print("Make sure 'pyserial' is installed and the port is correct.")
    finally:
        if 'ser' in locals() and ser.is_open:
            ser.close()
            print("Serial connection closed.")

if __name__ == '__main__':
    main()