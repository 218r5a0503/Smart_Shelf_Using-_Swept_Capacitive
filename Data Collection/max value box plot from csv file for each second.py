import pandas as pd
import matplotlib.pyplot as plt
import os

# === File Info ===
csv_filename = "Serial_data_G9P1.csv"
folder_path = "/Users/molaymondal/Desktop/EVERY GREED TOUCH DATA/G9"
csv_path = os.path.join(folder_path, csv_filename)

try:
    # Load CSV
    df = pd.read_csv(csv_path)

    if "Timestamp" not in df.columns or "Serial Data" not in df.columns:
        raise ValueError("Missing 'Timestamp' or 'Serial Data' column in CSV.")

    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    df['Second'] = df['Timestamp'].dt.floor('s')

    grouped = df.groupby('Second')
    boxplot_data = []
    second_labels = []

    for second, group in grouped:
        top_values = []

        for row in group['Serial Data']:
            try:
                values = list(map(int, row.split(',')))
                top_two = sorted(values, reverse=True)[:2]
                top_values.extend(top_two)
            except Exception as e:
                print(f"Skipping invalid row: {e}")

        if top_values:
            boxplot_data.append(top_values)
            second_labels.append(second.strftime('%H:%M:%S'))

    if not boxplot_data:
        print("❌ No valid data to plot.")
    else:
        plt.figure(figsize=(14, 6))
        plt.boxplot(boxplot_data, labels=second_labels, showfliers=False)
        plt.xticks(rotation=45)
        plt.title("Box Plot of Top 2 Sensor Values Per Second")
        plt.xlabel("Timestamp (per second)")
        plt.ylabel("Sensor Values")
        plt.grid(True)
        plt.tight_layout()

        # Save plot
        plot_filename = "Top2_BoxPlot_Per_Second.png"
        plot_path = os.path.join(folder_path, plot_filename)
        plt.savefig(plot_path)
        plt.show()

        print(f"✅ Box plot saved to: {plot_path}")

except FileNotFoundError:
    print(f"❌ File not found: {csv_path}")
except Exception as e:
    print(f"❌ Error: {e}")