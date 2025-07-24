import serial.tools.list_ports
import csv
import matplotlib.pyplot as plt
import random
import time
import sys

plt.ion()  # Enable interactive plotting

# Initialize serial connection
ports = serial.tools.list_ports.comports()
serialInst = serial.Serial()
portList = []

# List available ports and ask user to select one
for onePort in ports:
    portList.append(str(onePort))
    print(str(onePort))

val = input("Select port COM:")

# Find the selected COM port
for x in range(0, len(portList)):
    if portList[x].startswith("COM" + str(val)):
        portVar = "COM" + str(val)
        print("Selected port:", portVar)

# Set up serial connection
serialInst.baudrate = 9600
serialInst.port = portVar
serialInst.open()

# Prepare CSV file for writing
with open("Serial_data.csv", mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Serial Data"])  # Writing header

    # Initialize data list for plotting
    data_list = []
    
    try:
        while True:
            if serialInst.in_waiting:
                packet = serialInst.readline()
                data = packet.decode('utf-8').rstrip('\n')
                print(data)
                
                # Write data to CSV
                writer.writerow([data])

                # Add data to the list for plotting
                try:
                    # If the data is numeric, convert it to float
                    data_value = float(data)
                    data_list.append(data_value)

                    # Limit the length of data for efficient plotting
                    if len(data_list) > 50:  # Show last 50 data points
                        data_list.pop(0)

                    # Clear the current plot and plot new data
                    plt.clf()
                    plt.plot(data_list)
                    plt.xlabel('Time')
                    plt.ylabel('Value')
                    plt.title('Real-time Serial Data Plot')
                    plt.draw()
                    plt.pause(0.1)  # Pause to update the plot

                except ValueError:
                    print(f"Non-numeric data received: {data}")

    except KeyboardInterrupt:
        print("Terminating program.")
    finally:
        # Close serial connection gracefully
        serialInst.close()
        plt.ioff()  # Turn off interactive mode
        plt.show()  # Show the final plot
