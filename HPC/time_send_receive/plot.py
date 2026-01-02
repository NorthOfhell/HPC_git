import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Read Excel file
file_path = r"time_send_receive.xlsx"
df = pd.read_excel(file_path, sheet_name="Blad2")

# Convert decimal commas to points if necessary
for col in df.columns[1:]:
    df[col] = df[col].astype(str).str.replace(',', '.').astype(float)

# Convert Elements (ints) to Bytes
df['Bytes'] = df['Elements'] * 4  # sizeof(int) = 4 bytes

# Function to fit a + b*x using least squares (x in BYTES)
def fit_interval(df, col, start_bytes, end_bytes):
    subset = df[(df['Bytes'] >= start_bytes) & (df['Bytes'] <= end_bytes)]
    x = subset['Bytes'].values
    y = subset[col].values

    x_mean = np.mean(x)
    y_mean = np.mean(y)

    b = np.sum((x - x_mean) * (y - y_mean)) / np.sum((x - x_mean)**2)
    a = y_mean - b * x_mean
    return a, b

# Define intervals in BYTES
intervals = [
    (4 * 1,      4 * 2**8),
    (4 * 2**8,   4 * 2**13),
    (4 * 2**13,  4 * 2**20)
]

# Single log-log plot
plt.figure(figsize=(10, 6))

for col in df.columns[1:-1]:
    plt.plot(df['Bytes'], df[col], marker='o', linestyle='-', label=col)

    # Add fitted lines
    for (start, end) in intervals:
        a, b = fit_interval(df, col, start, end)
        x_fit = np.logspace(np.log10(start), np.log10(end), 200)
        y_fit = a + b * x_fit

        print(f"{col}, interval [{start},{end}] bytes: a = {a:.3e}, b = {b:.3e} s/byte")
        #plt.plot(x_fit, y_fit, '--')

plt.xlabel('Message size (bytes)')
plt.ylabel('Time (seconds)')
plt.title('Ping-Pong Communication Time (log-log)')
plt.xscale('log')
plt.yscale('log')
plt.grid(True)
plt.legend()
plt.savefig("timing_logscale_fits.png", dpi=600)
plt.show()