import matplotlib.pyplot as plt
import numpy as np

filename = "data/1.2.11"

with open(filename) as f:
    lines = [line.strip() for line in f if line.strip()]

# split file into two parts
split_index = lines.index("4 1")
data1 = lines[1:split_index]
data2 = lines[split_index + 1:]

# convert each part to float arrays
x1, y1, z1 = np.loadtxt(data1, unpack=True)
x2, y2, z2 = np.loadtxt(data2, unpack=True)

for i in range(len(x1)):
    x1[i] = 2*x1[i]

for i in range(len(x2)):
    x2[i] = 2*x2[i] * 3

a,b = np.polyfit(x1, y1, 1)
print(a,b)
plt.figure()
plt.plot(x1,y1)
plt.plot(x1,  a* x1 + b)
plt.show()


a,b = np.polyfit(x2, y2, 1)
print(a,b)
plt.figure()
plt.plot(x1,y1)
plt.plot(x1,  a* x1 + b)
plt.show()