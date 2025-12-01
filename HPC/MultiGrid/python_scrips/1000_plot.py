import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

# --- Data ---
grid_sizes = np.array([4, 8, 16, 32, 64])
max_computation_times = np.array([12.967653, 7.078562, 3.962451, 2.457001, 1.195644])
max_exchange_plus_global = np.array([0.075248, 0.183319, 0.291383, 0.237179, 0.685707])

# --- Model Definitions ---
# Power-law / exponential-like model for computation time: y = a * x^b + c
def power_law_model(x, a, b, c):
    return a * x**b + c

# Polynomial degree for exchange+global
poly_degree = 1

# --- Curve Fitting ---
# Fit for max computation time
popt_comp, _ = curve_fit(power_law_model, grid_sizes, max_computation_times, p0=(10, -0.5, 0))

# Polynomial fit for max exchange+global
poly_coeffs = np.polyfit(grid_sizes, max_exchange_plus_global, poly_degree)
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
plt.plot(grid_sizes, max_computation_times, 'o', markersize=6, label='Computation data', color='tab:blue')
plt.plot(x_fit, y_comp_fit, '-', linewidth=2, label=f'Computation Exponential Fit', color='tab:blue')

plt.plot(grid_sizes, max_exchange_plus_global, 's', markersize=6, label='Communication data', color='tab:orange')
plt.plot(x_fit, y_exch_fit, '--', linewidth=2, label=f'Communication Polynomial Fit ', color='tab:orange')

plt.xlabel("Grid Size", fontsize=12)
plt.ylabel("Time (s)", fontsize=12)
plt.title("Computation vs Communication Times", fontsize=14)
plt.legend(fontsize=10)
plt.tight_layout()
plt.savefig("plots/1000_plot.png", dpi=300)
plt.show()

# --- Print Fitted Parameters ---
print("Max Computation Time Power-law Fit Parameters: a, b, c =", popt_comp)
print("Max Exchange+Global Polynomial Fit Coefficients:", poly_coeffs)
