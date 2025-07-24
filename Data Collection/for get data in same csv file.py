import serial
import csv
import time
import matplotlib.pyplot as plt
from datetime import datetime
import os
from serial.tools import list_ports

print("Current Working Directory:", os.getcwd())

grid_no = input("Enter Grid No: ").strip()
user_name = input("Enter User Name: ").strip()
location = input("Enter Location: ").strip()
scenario = input("Enter Scenario: ").strip()

available_ports = list(list_ports.comports())
if not available_ports:
    print("No serial ports found. Please connect your device and try again.")
    exit()

print("\nAvailable Serial Ports:")
for i, port in enumerate(available_ports):
    print(f"{i + 1}: {port.device} ({port.description})")

port_index = input("Select port number from the list above: ").strip()
if port_index.isdigit() and 1 <= int(port_index) <= len(available_ports):
    SERIAL_PORT = available_ports[int(port_index) - 1].device
else:
    SERIAL_PORT = available_ports[0].device  

print(f"Using serial port: {SERIAL_PORT}")
BAUD_RATE = 115200

CSV_FILE = os.path.expanduser("~/Desktop/Serial_data.csv")

plt.ion()
fig, ax = plt.subplots()
x_data = list(range(1, 252))
latest_data = [0] * len(x_data)
line, = ax.plot(x_data, latest_data)
ax.set_title("Real-Time Serial Data Plot")
ax.set_xlabel("Data Index (1 to 251)")
ax.set_ylabel("Sensor Values")
ax.grid(True)

try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    print(f"Connected to {SERIAL_PORT} at {BAUD_RATE} baud.")

    try:
        with open(CSV_FILE, mode="a", newline="") as file:
            writer = csv.writer(file)

            if os.stat(CSV_FILE).st_size == 0:
                writer.writerow(["Timestamp", "Grid No", "User Name", "Location", "Scenario", "Serial Data"])

            while True:
                try:
                    line_raw = ser.readline().decode("utf-8", errors="ignore").strip()
                    if not line_raw:
                        continue

                    print(f"Raw Data: {line_raw}")

                    data_values = [int(x) for x in line_raw.split(',') if x.strip().isdigit()]

                    if len(data_values) != len(x_data):
                        print(f"Data length mismatch (Expected {len(x_data)}, Got {len(data_values)}), skipping.")
                        continue

                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                    writer.writerow([timestamp, grid_no, user_name, location, scenario, ','.join(map(str, data_values))])
                    file.flush()
                    print(f"Data saved at {timestamp}")

                    latest_data = data_values
                    line.set_ydata(latest_data)
                    ax.relim()
                    ax.autoscale_view()
                    plt.draw()
                    plt.pause(0.1)

                except KeyboardInterrupt:
                    print("\nUser stopped the script.")
                    break
                except Exception as e:
                    print(f"Error: {e}")
    except Exception as file_error:
        print(f"File writing error: {file_error}")

except Exception as e:
    print(f"Serial connection failed: {e}")
    print("Make sure 'pyserial' is installed and you're not using a file named 'serial.py'.")

finally:
    if 'ser' in locals() and ser.is_open:
        ser.close()
        print("Serial connection closed.")