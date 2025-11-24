import numpy as np
import os

filename = "data/1.2.3_only_computation"
with open(filename, 'r') as f:
    lines = [line.strip() for line in f if line.strip()]

sections = []
current_title = None
current_data = []

for line in lines:
    if all(part.isdigit() for part in line.split()):  # title line
        if current_title and current_data:
            sections.append((current_title, np.array(current_data)))
        current_title = line
        current_data = []
    else:
        x_str, y_str = line.split(':')
        x = float(x_str)
        y = float(y_str)
        current_data.append([x, y])

# Add the last section
if current_title and current_data:
    sections.append((current_title, np.array(current_data)))

# Fit lines
results = {}
for title, data in sections:
    x = data[:, 0]
    y = data[:, 1]
    a, b = np.polyfit(x, y, 1)
    results[title] = (a, b)

print(results)