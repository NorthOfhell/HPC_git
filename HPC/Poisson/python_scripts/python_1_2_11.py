from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np

def read_and_average(filename):
    data = defaultdict(list)

    with open(filename, "r") as f:
        for line in f:
            if not line.strip():
                continue

            a, b, grid_size, iterations, time = line.split()
            key = (int(a), int(b), int(grid_size), int(iterations))
            data[key].append(float(time))

    results = []
    for key, times in data.items():
        mean_time = sum(times) / len(times)
        results.append((*key, mean_time))

    return results


if __name__ == "__main__":
    filename = "data//comm_4_1_1.0000.dat"   # change if needed
    results = read_and_average(filename)

    plot_data = {}
    for a, b, grid_size, iterations, mean_time in results:
        if (a == 4 and b == 1):
            # 4 bytes is one float grid size for one border, we transfer data over 2 boarders, and receive over 2 boarders
            total_data = 4 * grid_size * 4
        else:
            print("error")

        print(total_data)
        if grid_size in plot_data:
            plot_data[grid_size].append((iterations * total_data, mean_time))
        else:
            plot_data[grid_size] = [(iterations * total_data, mean_time)]


    for grid_size, values in plot_data.items():
        values.sort()
        iterations, mean_times = zip(*values)

        iterations = np.array(iterations)
        mean_times = np.array(mean_times)

        # linear fit: y = m x + c
        m, c = np.polyfit(iterations, mean_times, 1)

        print(f"grid size {grid_size}: slope = {m}, intercept = {c}")

        fit = m * iterations + c

        plt.scatter(iterations, mean_times, label=f"data (grid {grid_size})")
        plt.plot(iterations, fit, linestyle='--',
                label=f"fit (grid {grid_size})")

        plt.xlabel("bytes")
        plt.ylabel("time")
        plt.legend()
        plt.grid(True)
        plt.show()