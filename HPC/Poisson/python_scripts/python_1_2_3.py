import numpy as np
import os
import matplotlib.pyplot as plt

filename = "data/1.2.3_only_computation"

sections = []
gridsize = None
grid_setup = None
with open(filename, 'r') as f:
    lines = [line.strip() for line in f if line.strip()]

    for line in lines:
        if all(part.isdigit() for part in line.split()):  # title line

            if gridsize and grid_setup and current_data:
                sections.append((gridsize, grid_setup, np.array(current_data)))
            gridsize = line.split()[0]
            grid_setup = line.split()[1] + line.split()[2]
            current_data = []
        else:
            x_str, y_str = line.split(':')
            x = float(x_str)
            y = float(y_str)
            current_data.append([x, y])
    
# Add the last section
if gridsize and grid_setup and current_data:
    sections.append((gridsize, grid_setup, np.array(current_data)))

# Fit lines
results = {}
for gridsize, grid_setup, data in sections:
    x = data[:, 0]
    y = data[:, 1]
    a, b = np.polyfit(x, y, 1)

    if grid_setup not in results:
        results[grid_setup] = []

    results[grid_setup].append((gridsize, a, b))

    x_fit = np.linspace(x.min(), x.max(), 200)
    y_fit = a * x_fit + b

    plt.figure()
    plt.scatter(x,y)
    plt.plot(x_fit, y_fit)
    plt.title( f"{gridsize} {grid_setup}")
    plt.show()

for grid_setup, entries in results.items():
    print(f"Grid setup: {grid_setup}")
    print(f"{'Gridsize':>10} | {'a':>12} | {'b':>12}")
    print("-" * 60)
    for gridsize, a, b in entries:
        print(f"{gridsize:10} | {a:12.6e} | {b:12.6e}")
    print()  # blank line between setups