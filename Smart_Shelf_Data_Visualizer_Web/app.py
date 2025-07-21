from flask import Flask, render_template, send_file, jsonify, send_from_directory
import csv
from datetime import datetime
import os
import threading
import time
import random
import matplotlib
matplotlib.use('Agg')  # Set the backend to Agg
import matplotlib.pyplot as plt
from io import BytesIO
import base64

app = Flask(__name__, static_folder='static', template_folder='templates')
CSV_FILE = "Serial_data.csv"

# Simulated data storage
latest_data = []
data_lock = threading.Lock()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/plot')
def get_plot():
    try:
        with data_lock:
            # Read data from CSV
            data_points = []
            if os.path.exists(CSV_FILE):
                with open(CSV_FILE, 'r') as file:
                    reader = csv.reader(file)
                    next(reader, None)  # Skip header
                    for row in reader:
                        if len(row) >= 2:
                            values = row[1].split(',')
                            if values and values[0].isdigit():
                                data_points.extend(map(int, values))
            
            if not data_points:
                return "No data available", 404

            # Create plot
            plt.figure(figsize=(10, 5))
            plt.plot(data_points[-251:])  # Show last 251 points
            plt.title("Serial Data Visualization")
            plt.xlabel("Data Index")
            plt.ylabel("Sensor Value")
            plt.grid(True)
            
            # Save plot to a buffer
            buf = BytesIO()
            plt.savefig(buf, format='png')
            plt.close()
            buf.seek(0)
            
            # Convert to base64 for HTML
            plot_data = base64.b64encode(buf.getvalue()).decode('utf-8')
            return jsonify({'plot': plot_data})
            
    except Exception as e:
        print(f"Error generating plot: {e}")
        return "Error generating plot", 500

@app.route('/download')
def download_csv():
    if os.path.exists(CSV_FILE):
        return send_file(CSV_FILE, as_attachment=True)
    return "No data available", 404

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory(app.static_folder, filename)

def run_serial_reader():
    """Simulate data if real serial data isn't available"""
    while True:
        time.sleep(0.1)
        with data_lock:
            # Generate simulated data
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            simulated_data = [random.randint(20, 80) for _ in range(251)]
            
            # Write to CSV
            with open(CSV_FILE, 'a', newline='') as file:
                writer = csv.writer(file)
                if os.stat(CSV_FILE).st_size == 0:
                    writer.writerow(["Timestamp", "Serial Data"])
                writer.writerow([timestamp, ','.join(map(str, simulated_data))])

if __name__ == '__main__':
    # Create CSV file if it doesn't exist
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Timestamp", "Serial Data"])
    
    # Start data generator in a separate thread
    data_thread = threading.Thread(target=run_serial_reader, daemon=True)
    data_thread.start()
    
    app.run(debug=True, port=5000, use_reloader=False)