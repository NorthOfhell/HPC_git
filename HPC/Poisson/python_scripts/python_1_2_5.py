import numpy as np
import matplotlib.pyplot as plt

x = []
y = []
filename = "data/1.2.5"
with open(filename) as f:
    for line in f:
        print(line)
        a = line.split()
        x.append(int(a[0]))
        y.append(int(a[1]))

a, b = np.polyfit(x, y, 1)
x = np.array(x)
y_line = x * a + b
plt.figure()
#plt.plot(x,y_line, ls="--", c="black")
plt.xlabel("gridsize")
plt.ylabel("iterations")
plt.scatter(x,y, marker='o')
plt.savefig("1_2_5.png", dpi=600)
plt.show()

print(a,b)
