import matplotlib.pyplot as plt
import numpy as np


speedup = []
data_measurements = ("2000", "1000", "100", "500")
for string in data_measurements:
    data = {}
    time_serial = []
    with open("data_serial_" + string + ".txt","r") as file:
        a = file.read()
        a = a.split("\n")
        for line in a:
            data_elements = line.split(",")
            time_serial.append(abs(float(data_elements[1].split(":")[1].strip())))




    with open("data_parallel_" + string + ".txt","r") as file:
        a = file.read()
        a = a.split("\n")
        for line in a:
            data_elements = line.split(",")
            time = float(data_elements[1].split(":")[1].strip())
            processors = int(data_elements[2].split(":")[1].strip())

            if processors in data:
                data[processors] = min(data[processors], time)
            else:
                data[processors] = time

    x = sorted(data.keys())
    y = np.array([data[k] for k in x])

    speedup.append(min(time_serial) /y)
    print(y)
    plt.plot(x, y, marker="o", linestyle='dashed', label="measurements")
    plt.hlines(min(time_serial), min(x), max(x), colors="black", label=f"serial program: {min(time_serial):.4f} s")
    plt.title("square matrix-matrix product of size " + string)
    plt.xlabel("number of processors")
    plt.ylabel("time (s)")
    plt.xlim(1,65)
    plt.ylim(bottom=0)
    plt.legend()
    plt.savefig("MM_time_" + string, dpi=600)
    plt.clf()
    #plt.show()

plt.figure()
for index, _  in enumerate(speedup):
    plt.plot(x, speedup[index], label=data_measurements[index], marker="o")

plt.plot(x,x,linestyle='dashed', c="black")
plt.legend()
plt.xlabel("number of processors")
plt.ylabel("speedup")
plt.xlim(1,65)
plt.ylim(bottom=0)
plt.savefig("MM_speedup", dpi=600)
plt.show()