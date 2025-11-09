import numpy as np
import matplotlib.pyplot as plt
x = []
y = []
filename = "error/X_800_Y_800.dat"
with open(filename) as f:
    for line in f:
        a = line.split()
        x.append(int(a[0]))
        y.append(float(a[1]))

plt.figure()
plt.xlabel("iterations")
plt.ylabel("error")
plt.plot(x,y)
plt.yscale("log")
plt.savefig("1_2_6.png", dpi=600)
plt.show()
    