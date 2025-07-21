import serial
import csv
import time
import matplotlib.pyplot as plt
from datetime import datetime
import os

# === SETTINGS ===
SERIAL_PORT = "COM8"          # Change if needed
BAUD_RATE = 115200
CSV_FILE = "Serial_data.csv"

# === PLOT SETUP ===
plt.ion()
fig, ax = plt.subplots()
x = list(range(1, 251))       # X-axis: 1 to 250
latest_data = [0] * 250       # Initial Y-axis values
line, = ax.plot(x, latest_data)
ax.set_title("Real-Time Serial Data Plot")
ax.set_xlabel("Data Index (1 to 250)")
ax.set_ylabel("Sensor Values")
ax.grid(True)

# === SERIAL SETUP AND MAIN LOOP ===
try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    print(f"✅ Connected to {SERIAL_PORT} at {BAUD_RATE} baud.")

    # Open CSV file for appending
    file_exists = os.path.isfile(CSV_FILE)
    with open(CSV_FILE, mode="a", newline="") as file:
        writer = csv.writer(file)

        # Write header only once
        if not file_exists:
            writer.writerow(["Timestamp", "Serial Data"])

        while True:
            try:
                # Read and clean data from serial
                line_raw = ser.readline().decode("utf-8", errors="ignore").strip()
                if not line_raw:
                    continue

                print(f"📥 Raw Data: {line_raw}")

                # Convert string to list of integers
                data_values = [int(x) for x in line_raw.split(',') if x.strip().isdigit()]

                # Check if we received the expected number of values
                if len(data_values) < 250:
                    print(f"⚠️ Invalid data length ({len(data_values)}), skipping.")
                    continue

                # Write data to CSV with timestamp
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                writer.writerow([timestamp, ','.join(map(str, data_values))])
                file.flush()
                print(f"💾 Data saved at {timestamp}")

                # Update the plot
                latest_data = data_values
                line.set_ydata(latest_data)
                ax.relim()
                ax.autoscale_view()
                plt.draw()
                plt.pause(1)

            except KeyboardInterrupt:
                print("\n🛑 User stopped the script.")
                break
            except Exception as e:
                print(f"❌ Error while reading or plotting data: {e}")

except Exception as e:
    print(f"❌ Serial connection failed: {e}")
    print("⚠️ Make sure 'pyserial' is installed and no file is named 'serial.py' in your directory.")

finally:
    if 'ser' in locals() and ser.is_open:
        ser.close()
        print("🔌 Serial connection closed.")
