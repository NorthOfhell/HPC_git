import matplotlib.pyplot as plt


def parse_file(filename):
    results = {}  # key = grid size, value = list of dictionaries for each iteration

    with open(filename, "r") as f:
        current_grid = None
        for line in f:
            line = line.strip()
            if not line:
                continue

            # Grid size line, e.g., "100 141:"
            if line.endswith(":") and " " in line:
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

if __name__ == "__main__":
    filename = "results//4.2_1_4"
    name = filename.split("//")[1]
    numbers = name.split("_")
    data = parse_file(filename)
    compute_stats(data)

    grid_sizes = sorted(data.keys())

    # Compute average time per iteration for each component
    comp_times = [sum(e["computation"] for e in data[g])/len(data[g]) for g in grid_sizes]
    exchange_times = [sum(e["exchange"] for e in data[g])/len(data[g]) for g in grid_sizes]
    global_times = [sum(e["global"] for e in data[g])/len(data[g]) for g in grid_sizes]
    idle_times = [sum(e["idle"] for e in data[g])/len(data[g]) for g in grid_sizes]

    # Normalize so each bar adds up to 1
    totals = [c+e+g+i for c,e,g,i in zip(comp_times, exchange_times, global_times, idle_times)]
    comp_norm = [c/t for c,t in zip(comp_times, totals)]
    exchange_norm = [e/t for e,t in zip(exchange_times, totals)]
    global_norm = [g/t for g,t in zip(global_times, totals)]
    idle_norm = [i/t for i,t in zip(idle_times, totals)]

    # X positions (categorical)
    x = range(len(grid_sizes))
    width = 0.5  # bar thickness

    plt.figure(figsize=(8,6))
    plt.bar(x, comp_norm, width=width, label="Computation")
    plt.bar(x, exchange_norm, width=width, bottom=comp_norm, label="Exchange")
    plt.bar(x, global_norm, width=width, bottom=[c+e for c,e in zip(comp_norm, exchange_norm)], label="Global")
    plt.bar(x, idle_norm, width=width, bottom=[c+e+g for c,e,g in zip(comp_norm, exchange_norm, global_norm)], label="Idle")

    plt.xlabel("Grid size")
    plt.ylabel("fraction of total time")
    plt.title(f"Normalized time for a {numbers[1]}-{numbers[2]} grid")
    plt.xticks(x, grid_sizes)  # show actual grid sizes as labels
    plt.ylim(0,1)
    plt.legend()
    plt.grid(axis="y")
    plt.tight_layout()
    
    plt.savefig(f"plots//{name}.png", dpi=600)
    plt.show()