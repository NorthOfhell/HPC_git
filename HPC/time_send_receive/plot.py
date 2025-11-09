import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Replace 'your_file.xlsx' with the path to your Excel file
file_path = r"C:\Users\timov\OneDrive\HPC\time_send_receive\time_send_receive.xlsx"
# Read Excel file
df = pd.read_excel(file_path, sheet_name="Blad2")

# Convert decimal commas to points, if necessary
for col in df.columns[1:]:
    df[col] = df[col].astype(str).str.replace(',', '.').astype(float)

# Function to fit a + b*x using least squares
def fit_interval(df, col, start, end):
    subset = df[(df['Elements'] >= start) & (df['Elements'] <= end)]
    x = subset['Elements'].values
    y = subset[col].values

    x_mean = np.mean(x)
    y_mean = np.mean(y)

    b = np.sum((x - x_mean) * (y - y_mean)) / np.sum((x - x_mean)**2)
    a = y_mean - b * x_mean
    return a, b

# Define intervals
intervals = [
    (1, 2**8),
    (2**8, 2**13),
    (2**13, 2**20)
]

# Plot with log scales
plt.figure(figsize=(10, 6))
for col in df.columns[1:]:
    plt.plot(df['Elements'], df[col], marker='o', label=col)

    # Add fitted lines for each interval
    # for (start, end) in intervals:
    #     a, b = fit_interval(df, col, start, end)
    #     x_fit = np.linspace(start, end, 200)
    #     y_fit = a + b * x_fit
    #     print(col, a, b, start, end)
    #     plt.plot(x_fit, y_fit, '--', label=f"{col} fit [{start},{end}]")

plt.xlabel('Elements')
plt.ylabel('Time (seconds)')
plt.title('Ping Pong Timing (log-log with fits)')
plt.legend()
plt.grid(True)
plt.xscale('log')
plt.yscale('log')
plt.savefig("timing_logscale_fits.png", dpi=600)
plt.show()

# Plot with linear scales
plt.figure(figsize=(10, 6))
for col in df.columns[1:]:
    plt.plot(df['Elements'], df[col], marker='o', label=col)

    # Add fitted lines for each interval
    # for (start, end) in intervals:
    #     a, b = fit_interval(df, col, start, end)
    #     x_fit = np.linspace(start, end, 200)
    #     y_fit = a + b * x_fit
    #     plt.plot(x_fit, y_fit, '--', label=f"{col} fit [{start},{end}]")

plt.xlabel('Elements')
plt.ylabel('Time (seconds)')
plt.title('Ping Pong Timing (linear with fits)')
plt.legend()
plt.grid(True)
plt.savefig("timing_linearscale_fits.png", dpi=600)
plt.show()
