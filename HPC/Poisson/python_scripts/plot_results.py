import numpy as np
import matplotlib.pyplot as plt
import os

# ---------- USER PARAMETERS ----------
filenames = ["output1.dat", "output2.dat", "output3.dat", "output0.dat"]

filenames = ["output400.dat"]

# order: [top-left, top-right, bottom-left, bottom-right]

full_nx = full_ny = 400
tiles_x = tiles_y = 1   # 2x2 tile layout
dtype_save = np.float32  # save as float32 to reduce memory on disk
# -------------------------------------

tile_nx = full_nx // tiles_x
tile_ny = full_ny // tiles_y

if full_nx % tiles_x != 0 or full_ny % tiles_y != 0:
    raise ValueError("full size not divisible by tile counts")

def read_tile(fname):
    """
    Attempts to read a tile file in either of these formats:
     - three columns: x y value  (x,y integers indexing into global grid)
     - single column: value (row-major order for the tile)
    Returns: a 2D numpy array of shape (tile_ny, tile_nx)
    """
    # Try to read a few lines to detect columns / header
    with open(fname, "r") as f:
        # skip blank lines and comments at top
        sample_lines = []
        for _ in range(10):
            line = f.readline()
            if not line:
                break
            line_strip = line.strip()
            if line_strip == "" or line_strip.startswith("#") or line_strip.lower().startswith("x"):
                continue
            sample_lines.append(line_strip)
        if not sample_lines:
            raise ValueError(f"file {fname} appears empty or only comments")

    # determine column count by splitting first non-empty data line
    first = sample_lines[0].split()
    ncols = len(first)

    if ncols >= 3:
        # treat as x y value (may be global x,y coordinates)
        data = np.loadtxt(fname)
        if data.ndim == 1:
            # single line only
            data = data.reshape((1, -1))
        x = data[:,0].astype(int)
        y = data[:,1].astype(int)
        val = data[:,2].astype(float)

        # If x,y look like local indices (0..tile_nx-1 etc) OR global (0..full_nx-1)
        x_min, x_max = x.min(), x.max()
        y_min, y_max = y.min(), y.max()

        # Decide if coordinates are local (0..tile_nx-1) by checking ranges
        if 0 <= x_min <= x_max < tile_nx and 0 <= y_min <= y_max < tile_ny:
            # local indices: we assume tile file corresponds to a single tile and
            # will be placed entirely into its quadrant (so x,y are local)
            grid = np.full((tile_ny, tile_nx), np.nan, dtype=float)
            grid[y, x] = val
            return grid

        # If coordinates are global (0..full_nx-1), create a tile by selecting points
        # The caller will place values by coordinates in the global grid.
        return ("global_xyz", x, y, val)

    elif ncols == 1:
        # single column -> values only, row-major for the tile
        vals = np.loadtxt(fname, dtype=float)
        if vals.size != tile_nx * tile_ny:
            raise ValueError(f"file {fname} expected {tile_nx*tile_ny} values, got {vals.size}")
        tile = vals.reshape((tile_ny, tile_nx))
        return tile
    else:
        raise ValueError(f"unhandled column count ({ncols}) in {fname}")

# Prepare the big grid
big = np.full((full_ny, full_nx), np.nan, dtype=float)

# mapping of tile index to (tile_row, tile_col) for order: TL, TR, BL, BR
tile_positions = [(0,0), (0,1), (1,0), (1,1)]

# track if any file provided global_xyz data
global_xyz_entries = []

for fname, (trow, tcol) in zip(filenames, tile_positions):
    if not os.path.exists(fname):
        raise FileNotFoundError(f"File not found: {fname}")
    tile_data = read_tile(fname)

    if isinstance(tile_data, tuple) and tile_data[0] == "global_xyz":
        # Defer placing - collect global coordinate data
        _, xg, yg, vg = tile_data
        global_xyz_entries.append((xg, yg, vg))
        continue

    # tile_data is a 2D tile of shape (tile_ny, tile_nx)
    y0 = trow * tile_ny
    y1 = y0 + tile_ny
    x0 = tcol * tile_nx
    x1 = x0 + tile_nx
    big[y0:y1, x0:x1] = tile_data

# If any global coordinate data present, place them into the big grid
# place global coordinate data into big safely (handles 1-based coords)
for xg, yg, vg in global_xyz_entries:
    xg = np.asarray(xg)  # ensure numpy array
    yg = np.asarray(yg)
    vg = np.asarray(vg)

    # convert from 1-based to 0-based indices
    x0 = (xg - 1).astype(np.intp)
    y0 = (yg - 1).astype(np.intp)

    # bounds check for 0-based indexing
    if x0.min() < 0 or x0.max() >= full_nx or y0.min() < 0 or y0.max() >= full_ny:
        raise ValueError(f"global coordinates out of bounds after converting to 0-based: "
                         f"x range {x0.min()}..{x0.max()}, y range {y0.min()}..{y0.max()} "
                         f"(expected 0..{full_nx-1}, 0..{full_ny-1})")

    # Now assign. If x0 and y0 are 1D arrays of equal length, this indexes elementwise.
    big[y0, x0] = vg

# Optional: check for any remaining NaNs
n_missing = np.isnan(big).sum()
if n_missing:
    print(f"Warning: assembled grid contains {n_missing} missing values (NaN).")


# Quick visualization: downsample with block averaging for viewing
def block_mean(a, block):
    ny, nx = a.shape
    ny_trim = (ny // block) * block
    nx_trim = (nx // block) * block
    a2 = a[:ny_trim, :nx_trim]
    a2 = a2.reshape(ny_trim//block, block, nx_trim//block, block)
    return a2.mean(axis=(1,3))

# choose block so the image is reasonable on screen (e.g. 800x800)
block = full_nx // 800
if block < 1:
    block = 1

grid_coarse = 4 * block_mean(big, block=block)
plt.figure(figsize=(6,6))
plt.imshow(grid_coarse, origin="lower", interpolation="nearest")
plt.title(f"Downsampled view (block={block})")
plt.colorbar(label="value")
plt.savefig(f"grid_{full_nx}.png")
plt.show()