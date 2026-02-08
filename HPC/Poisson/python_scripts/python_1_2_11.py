from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np

def read_and_average1(filename):
    data = defaultdict(list)

    with open(filename, "r") as f:
        for line in f:
            if not line.strip():
                continue

            a, b, grid_size, iterations, time_full, time0, time1, time2, time3 = line.split()
            key = (int(a), int(b), int(grid_size), int(iterations))
            data[key].append(float(time1))

    results = []
    for key, times in data.items():
        mean_time = sum(times) / len(times)
        results.append((*key, mean_time))

    return results



def read_and_average2(filename):
    data = defaultdict(list)

    with open(filename, "r") as f:
        for line in f:
            if not line.strip():
                continue

            a, b, grid_size, iterations, time_full, time0, time1, time2, time3 = line.split()
            key = (int(a), int(b), int(grid_size), int(iterations))
            data[key].append(float(time1) + float(time3))

    results = []
    for key, times in data.items():
        mean_time = sum(times) / len(times)
        results.append((*key, mean_time))

    return results


if __name__ == "__main__":
    filename = "data//comm_4_1_1.0000.dat"   # change if needed
    filename1 = "data//comm_2_2_1.0000.dat"   # change if needed
    results = read_and_average1(filename)
    results1 = read_and_average2(filename1)

    plot_data = {}
    plot_data1 = {}
    for a, b, grid_size, iterations, mean_time in results:
        if (a == 4 and b == 1):
            # 4 bytes is one float grid size for one border, we transfer data over 2 boarders, and receive over 2 boarders
            total_data = 3 * grid_size * 4
        elif(a == 2 and b == 2):
            total_data =  2 * grid_size * 4
        else:
            print("error")
        
        if grid_size in plot_data:
            plot_data[grid_size].append((iterations * total_data, mean_time))
        else:
            plot_data[grid_size] = [(iterations * total_data, mean_time)]


    for a, b, grid_size, iterations, mean_time in results1:
        if (a == 4 and b == 1):
            # 4 bytes is one float grid size for one border, we transfer data over 2 boarders, and receive over 2 boarders
            total_data = 3 * grid_size * 4
        elif(a == 2 and b == 2):
            total_data =  grid_size * 4
        else:
            print("error")
        
        if grid_size in plot_data1:
            plot_data1[grid_size].append((iterations * total_data, mean_time))
        else:
            plot_data1[grid_size] = [(iterations * total_data, mean_time)]



split_index = 3  # change this to set how many points go into the first fit


for grid_size in plot_data.keys():
    # First file
    values = plot_data[grid_size]
    values.sort()
    bytes_sent, mean_times = zip(*values)
    bytes_sent = np.array(bytes_sent)
    mean_times = np.array(mean_times)

    # Second file
    values1 = plot_data1[grid_size]
    values1.sort()
    bytes_sent1, mean_times1 = zip(*values1)
    bytes_sent1 = np.array(bytes_sent1)
    mean_times1 = np.array(mean_times1)

    # --- Continuous x-range for fits ---
    # First dataset
    first_bytes = bytes_sent[:split_index]
    rest_bytes = bytes_sent[split_index:]
    first_times = mean_times[:split_index]
    rest_times = mean_times[split_index:]

    m_first, c_first = np.polyfit(first_bytes, first_times, 1)
    m_rest, c_rest = np.polyfit(rest_bytes, rest_times, 1)

    # Create continuous x-values for plotting so lines meet
    x_first = np.linspace(0, first_bytes[-1], 50)
    fit_first = m_first * x_first + c_first
    x_rest = np.linspace(rest_bytes[0], rest_bytes[-1], 50)
    fit_rest = m_rest * x_rest + c_rest

    # Second dataset
    first_bytes1 = bytes_sent1[:split_index]
    rest_bytes1 = bytes_sent1[split_index:]
    first_times1 = mean_times1[:split_index]
    rest_times1 = mean_times1[split_index:]

    m1_first, c1_first = np.polyfit(first_bytes1, first_times1, 1)
    m1_rest, c1_rest = np.polyfit(rest_bytes1, rest_times1, 1)

    x1_first = np.linspace(0, first_bytes1[-1], 50)
    fit1_first = m1_first * x1_first + c1_first
    x1_rest = np.linspace(rest_bytes1[0], rest_bytes1[-1], 50)
    fit1_rest = m1_rest * x1_rest + c1_rest

    print(f"Grid {grid_size} 4x1: first fit slope/intercept = {m_rest}, {c_first}")
    print(f"Grid {grid_size} 2x2: first fit slope/intercept = {m1_rest}, {c1_first}")

    # --- Plot ---
    plt.scatter(bytes_sent[:split_index], mean_times[:split_index], label=f"4 x 1 data (grid {grid_size})")
    plt.plot(x_first, fit_first, '--', label=f"4 x 1 latency fit")
    

    
    plt.scatter(bytes_sent1[:split_index], mean_times1[:split_index], label=f"2 x 2 data (grid {grid_size})")
    plt.plot(x1_first, fit1_first, '--', label=f"2 x 2 latency fit")

    plt.xlabel("bytes")
    plt.ylabel("time")
    plt.title(f"Grid size {grid_size}")
    plt.legend()
    plt.grid(True)
    plt.savefig(f"grid_plot//11_{grid_size}_latency.png", dpi=600)
    plt.show()

    plt.scatter(bytes_sent[split_index:], mean_times[split_index:], label=f"4 x 1 data (grid {grid_size})")
    plt.scatter(bytes_sent1[split_index:], mean_times1[split_index:], label=f"2 x 2 data (grid {grid_size})")
    plt.plot(x1_rest, fit1_rest, '--', label=f"2 x 2 bandwidth fit")
    plt.plot(x_rest, fit_rest, '--', label=f"4 x 1 bandwidth fit")
    plt.xlabel("bytes")
    plt.ylabel("time")
    plt.title(f"Grid size {grid_size}")
    plt.legend()
    plt.grid(True)
    plt.savefig(f"grid_plot//11_{grid_size}_bandwidth.png", dpi=600)
    plt.show()