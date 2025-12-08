import matplotlib.pyplot as plt
import os
import numpy as np

directory = "plot_output_files"
files = os.listdir(directory)

max_x = 0
max_y = 0

for i in files:
    with open(directory + "//" + i) as f:
        lines = f.readlines()
        last_line = lines[-1]
        data = last_line.split()
        max_x = max(max_x, int(data[0]))
        max_y = max(max_y, int(data[1]))

phi = np.zeros(shape=(max_x, max_y))

for i in files:
    with open(directory + "//" + i) as f:
        for line in f:
            data = line.split()
            phi[int(data[0])-1, int(data[1]) - 1] = float(data[2])


plt.figure()
plt.imshow(phi)
plt.colorbar(label="value")
plt.show()



