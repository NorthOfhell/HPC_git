from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np

def read_and_average(filename):
    data = defaultdict(list)

    with open(filename, "r") as f:
        for line in f:
            if not line.strip():
                continue

            a, b, grid_size, iterations, time_full, time0, time1, time2, time3 = line.split()
            key = (int(a), int(b), int(grid_size), int(iterations))
            data[key].append(float(time1))
    
    print(data)
    results = []
    for key, times in data.items():
        mean_time = sum(times) / len(times)
        results.append((*key, mean_time))

    return results


if __name__ == "__main__":
    filename = "data//comm_4_1_1.0000.dat"   # change if needed
    results = read_and_average(filename)
    print(results)
    plot_data = {}
    for a, b, grid_size, iterations, mean_time in results:
        if (a == 4 and b == 1):
            # 4 bytes is one float grid size for one border, we transfer data over 2 boarders, and receive over 2 boarders
            total_data = 3 * grid_size * iterations
            plot_data[grid_size] = mean_time/total_data
            
        elif (a == 2 and b == 2):
            print("not good")
            total_data = grid_size * iterations
            plot_data[grid_size] = mean_time/total_data
        else:
            print("error")


    grid_sizes = np.array(list(plot_data.keys()))
    time_per_byte = np.array(list(plot_data.values()))

    print(grid_sizes, time_per_byte)
    m, c = np.polyfit(grid_sizes, time_per_byte, 1)

    m, c = np.polyfit(grid_sizes, time_per_byte, 1)
    fit = m * grid_sizes + c

    plt.scatter(grid_sizes, time_per_byte, label="data")
    plt.plot(grid_sizes, fit, '--', label="linear fit")

    plt.xlabel("grid size")
    plt.ylabel("time per byte")
    plt.legend()
    plt.grid(True)
    plt.show()