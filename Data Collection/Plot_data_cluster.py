import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import os

# Load CSV file
CSV_FILE = os.path.expanduser("Serial_data_On_metal_table.csv")
df = pd.read_csv(CSV_FILE)

# Drop incomplete rows
df.dropna(subset=["Grid No", "Serial Data"], inplace=True)

# Group by Grid No
grid_groups = df.groupby("Grid No")

# Define custom colors
color_map_by_grid = {
    "G1": "red",
    "G2": "blue",
    "G3": "green",
    "G4": "orange",
    "G5": "pink",
    "G6": "yellow",
    "G7": "grey",
    "G8": "black",
    "G9": "violet",
    "G10": "cyan"
}

# Prepare the combined plot
plt.figure(figsize=(10, 6))
plt.title("Clustered Sensor Data (All Grid Numbers Combined)")

for grid_no, group in grid_groups:
    # Convert 'Serial Data' to array
    data_matrix = group["Serial Data"].apply(
        lambda x: np.array([int(i) for i in x.split(",") if i.strip().isdigit()])
    )

    if len(data_matrix) < 10:
        print(f"Not enough data to cluster for Grid No: {grid_no}")
        continue

    data_array = np.vstack(data_matrix.values)

    # Apply KMeans clustering
    n_clusters = 10
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    labels = kmeans.fit_predict(data_array)

    # Choose color based on Grid No (if defined)
    color = color_map_by_grid.get(grid_no, None)

    for i in range(n_clusters):
        cluster_points = data_array[labels == i]
        plt.plot(
            cluster_points.T,
            alpha=0.4,
            label=f"{grid_no} - Cluster {i+1}" if not color else f"{grid_no}",
            color=color if color else None
        )

plt.xlabel("Sensor Index")
plt.ylabel("Sensor Value")
plt.legend()
plt.grid(True)
plt.tight_layout()

# Save plot to Desktop
save_path = os.path.expanduser("cluster_plot.png")
plt.savefig(save_path)
print(f"Plot saved to: {save_path}")

plt.show()
