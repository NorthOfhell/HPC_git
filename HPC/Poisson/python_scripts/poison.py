import numpy as np
from scipy.sparse import diags, kron, eye
from scipy.sparse.linalg import spsolve
import matplotlib.pyplot as plt

def poisson_fd_dirac(N, source_pos, obs_pos):
    """
    Solve 2D Poisson equation on a 1x1 domain with a point source (approx. Dirac)
    using a 5-point finite difference stencil and homogeneous Dirichlet BCs.
    
    Domain: (0,1)x(0,1). Interior grid has N x N points.
    
    Parameters
    ----------
    N : int
        Number of interior points per dimension.
    source_pos : [(x1, y1), ... ]
        Physical coordinates of the point source (both in (0,1)).
    obs_pos : (x, y)
        Physical coordinates of the observation point (both in (0,1)).
    
    Returns
    -------
    phi_obs : float
        Solution value at the observation location (nearest grid point).
    phi_grid : (N, N) ndarray
        Solution on the interior grid (phi_grid[i,j] corresponds to x[i], y[j]).
    x, y : 1D arrays
        Coordinates of the interior grid points (length N).
    """
    # grid and spacing
    h = 1.0 / (N + 1)
    x = np.linspace(h, 1.0 - h, N)
    y = np.linspace(h, 1.0 - h, N)
    
    # 1D second-derivative operator (tridiagonal: [1, -2, 1])
    main_1d = -2.0 * np.ones(N)
    off_1d = np.ones(N - 1)
    T = diags([off_1d, main_1d, off_1d], offsets=[-1, 0, 1], format='csr')
    I = eye(N, format='csr')
    
    # 2D Laplacian (kron sum). Scale by 1/h^2 so A u = f (discrete Laplacian).
    A = (kron(I, T) + kron(T, I))
    
    # right-hand side: approximate Dirac by putting cell-average = 1/h^2 at nearest grid cell
    b = np.zeros(N * N)
    for i in source_pos:
        src_i = int(np.argmin(np.abs(x - i[0])))
        src_j = int(np.argmin(np.abs(y - i[1])))
        src_idx = src_i * N + src_j
        b[src_idx] = 1.0    # ensures sum(b)*h^2 == 1.0 (unit-strength delta)
    print(A)
    # solve A phi = b
    phi = spsolve(A.tocsc(), b)   # use csc for spsolve efficiency
    phi_grid = phi.reshape((N, N))
    
    # observation
    obs_i = int(np.argmin(np.abs(x - obs_pos[0])))
    obs_j = int(np.argmin(np.abs(y - obs_pos[1])))
    phi_obs = phi_grid[obs_i, obs_j]
    
    return phi_obs, phi_grid, x, y

def poisson_sine_series(x0, y0, obs_pos, Nx=100, Ny=100, terms=50):
    """
    Compute Poisson equation solution on 1x1 square with Dirichlet BCs
    using sine series for a point source.
    """
    x = np.linspace(0, 1, Nx)
    y = np.linspace(0, 1, Ny)
    X, Y = np.meshgrid(x, y, indexing='ij')
    phi = np.zeros_like(X)
    
    for m in range(1, terms+1):
        for n in range(1, terms+1):
            if np.sin(m*np.pi*x0) == 0 or np.sin(n*np.pi*y0) == 0:
                continue
            phi += (4 / (np.pi**2 * (m**2 + n**2)) *
                    np.sin(m*np.pi*x0) * np.sin(n*np.pi*y0) *
                    np.sin(m*np.pi*X) * np.sin(n*np.pi*Y))
    
    # Find closest grid point to observation point
    obs_i = np.argmin(np.abs(x - obs_pos[0]))
    obs_j = np.argmin(np.abs(y - obs_pos[1]))
    phi_obs = phi[obs_i, obs_j]
    
    return phi_obs, X, Y, phi

# Parameters
source_pos = [(0.5, 0.5)]
obs_pos = (0.25, 0.25)
N_coarse = 100
N_fine = 1000

# Finite-difference solutions
coarse_val, coarse_grid, x_coarse, y_coarse = poisson_fd_dirac(N_coarse, source_pos, obs_pos)
#fine_val, fine_grid, x_fine, y_fine = poisson_fd_dirac(N_fine, source_pos, obs_pos)

print("Finite-difference (coarse 20x20) phi at observation:", coarse_val)
#print("Finite-difference (fine 100x100) phi at observation:", fine_val)

# # Sine-series solution
# phi_series_val, X_series, Y_series, phi_series = poisson_sine_series(source_pos[0], source_pos[1], obs_pos, Nx=200, Ny=200, terms=500)
# print("Sine-series solution phi at observation:", phi_series_val)

# Plot FD and sine-series solutions with proper aspect ratio
fig, axes = plt.subplots(1,2, figsize=(18,5))

# FD coarse
im0 = axes[0].imshow(coarse_grid, extent=[0,1,0,1], origin='lower')
axes[0].set_title("Finite-difference coarse grid")
axes[0].set_xlabel('x (m)')
axes[0].set_ylabel('y (m)')
axes[0].set_aspect('equal')
fig.colorbar(im0, ax=axes[0])
plt.show()
# # FD fine
# im1 = axes[1].imshow(fine_grid, extent=[0,1,0,1], origin='lower')
# axes[1].set_title("Finite-difference fine grid")
# axes[1].set_xlabel('x (m)')
# axes[1].set_ylabel('y (m)')
# axes[1].set_aspect('equal')
# fig.colorbar(im1, ax=axes[1])
# plt.show()

# result = []
# source = []
# size = 600
# for i in np.arange(20,size,20):
#     print(i)
#     coarse_val, _, _, _ = poisson_fd_dirac(i, source_pos, obs_pos)
#     result.append(coarse_val)

# plt.figure()
# plt.plot(np.arange(20,size,20), result)
# plt.show()

# plt.figure()
# plt.plot(np.arange(20,size,20), source)
# plt.show()