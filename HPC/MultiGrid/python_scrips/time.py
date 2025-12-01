import matplotlib.pyplot as plt

# Data stored directly in the script
groups = [10, 20, 30, 36, 40]
max_time_comp = [0.000034, 0.000199, 0.000632, 0.000950, 0.001275]
max_ex_glob = [0.000444, 0.000581, 0.000789, 0.000939, 0.000960]

# Plot
plt.figure()
plt.plot(groups, max_time_comp, label="time computation")
plt.plot(groups, max_ex_glob, label="time communicating")
plt.xlabel("grid size")
plt.ylabel("time(s)")
plt.legend()
plt.title("Computation vs communication")
plt.tight_layout()
plt.savefig("plots//1-4-time.png")
plt.show()