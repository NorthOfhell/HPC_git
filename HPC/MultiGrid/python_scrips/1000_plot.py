import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

# --- Data ---
def parse_file(filename):
    results = {}  # key = grid size, value = list of dictionaries for each iteration

    with open(filename, "r") as f:
        current_grid = None
        for line in f:
            line = line.strip()
            if not line:
                continue

            # Grid size line, e.g., "100 141:"
            if line.endswith(":"):
                parts = line[:-1].split()
                current_grid = int(parts[0])
                results[current_grid] = []
                continue

            # Timing line: split on commas, then on first ':' in each part
            if line.startswith("(") and "time computation" in line:
                parts = line.split(",")
                entry = {}
                for part in parts:
                    # split at the first colon
                    if ":" not in part:
                        continue
                    key_raw, value_raw = part.split(":", 1)
                    key = key_raw.strip()
                    value = float(value_raw.strip())

                    # remove leading "(...)" if present
                    if key.startswith("("):
                        close_idx = key.find(")")
                        if close_idx != -1:
                            key = key[close_idx+1:].strip()

                    # normalize to lower-case to avoid capitalization issues
                    key_norm = key.lower()

                    # match using substrings so minor formatting changes don't break parsing
                    if "computation" in key_norm:
                        entry["computation"] = value
                    elif "exchanging" in key_norm or "exchang" in key_norm or "exchange" in key_norm:
                        entry["exchange"] = value
                    elif "time global" in key_norm or "global" in key_norm:
                        entry["global"] = value
                    elif "idle" in key_norm:
                        entry["idle"] = value
                    elif "total" in key_norm:
                        entry["total"] = value

                # only append if we found something sensible (guard against malformed lines)
                if current_grid is not None and entry:
                    # ensure all keys exist (optional: skip incomplete entries)
                    for k in ("computation", "exchange", "global", "idle", "total"):
                        entry.setdefault(k, 0.0)
                    results[current_grid].append(entry)

    return results

def compute_stats(data):
    order = ["computation", "exchange", "global", "idle", "total"]
    for grid in sorted(data.keys()):
        entries = data[grid]
        print(f"Grid size {grid}:")
        for key in order:
            values = [e[key] for e in entries]
            print(f"  {key:12} min: {min(values):.4f}, avg: {sum(values)/len(values):.4f}")
        print()





# --- Model Definitions ---
# Power-law / exponential-like model for computation time: y = a * x^b + c
def power_law_model(x, a, b, c):
    return a * x**b + c

# Polynomial degree for exchange+global
poly_degree = 1


filename = "results\\1000-1-n-time.txt"
results = parse_file(filename)
print(results,"\n", results[2][0]["computation"])
grid_sizes = [key for key in results]
computation_time = [results[key][0]["computation"] for key in results]
communication_time = [results[key][0]["exchange"] + results[key][0]["global"] for key in results]

print(grid_sizes, computation_time, communication_time)
# --- Curve Fitting ---
# Fit for max computation time
popt_comp, _ = curve_fit(power_law_model, grid_sizes, computation_time, p0=(10, -0.5, 0))

# Polynomial fit for max exchange+global
poly_coeffs = np.polyfit(grid_sizes, communication_time, poly_degree)
poly_func = np.poly1d(poly_coeffs)

# --- Generate Smooth Curve for Plotting ---
x_fit = np.linspace(min(grid_sizes), 120, 200)
y_comp_fit = power_law_model(x_fit, *popt_comp)
y_exch_fit = poly_func(x_fit)

y_comp_fit = np.array(y_comp_fit)
y_exch_fit = np.array(y_exch_fit)
index = np.argmin(np.abs(y_comp_fit - y_exch_fit))
print(f"at {x_fit[index]} proccesors")
# --- Plot ---
plt.figure(figsize=(8, 5))
plt.plot(grid_sizes, computation_time, 'o', markersize=6, label='Computation data', color='tab:blue')
plt.plot(x_fit, y_comp_fit, '-', linewidth=2, label=f'Computation Exponential Fit', color='tab:blue')

plt.plot(grid_sizes, communication_time, 's', markersize=6, label='Communication data', color='tab:orange')
plt.plot(x_fit, y_exch_fit, '--', linewidth=2, label=f'Communication Polynomial Fit ', color='tab:orange')

plt.xlabel("Proccesors", fontsize=12)
plt.ylabel("Time (s)", fontsize=12)
plt.title("Computation vs Communication Times", fontsize=14)
plt.legend(fontsize=10)
plt.tight_layout()
plt.savefig("plots/1000_plot.png", dpi=300)
plt.show()

# --- Print Fitted Parameters ---
print("Max Computation Time Power-law Fit Parameters: a, b, c =", popt_comp)
print("Max Exchange+Global Polynomial Fit Coefficients:", poly_coeffs)
