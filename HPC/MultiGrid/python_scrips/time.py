import matplotlib.pyplot as plt

# Data stored directly in the script

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
    averages = {}
    order = ["computation", "exchange", "global", "idle", "total"]
    for grid in sorted(data.keys()):
        averages[grid] = []
        entries = data[grid]
        print(f"Grid size {grid}:")
        for key in order:
            values = [e[key] for e in entries]
            print(f"  {key:12} min: {min(values):.6f}, avg: {sum(values)/len(values):.6f}")
            averages[grid].append(sum(values)/len(values))
        print()
    return averages

data = parse_file("results//1-4-time.txt")
avarages = compute_stats(data)
values = 10
av_comp = []
av_comm = []
for grid in sorted(data.keys()):
    print()
    av_comp.append(avarages[grid][0])
    av_comm.append(avarages[grid][1] + avarages[grid][2])

for key, a,b in zip(sorted(data.keys()), av_comp, av_comm):
    print(f"{key} & {a:.6f} & {b:.6f} \\ \hline \n")
# Plot
print(av_comp, av_comm)
plt.figure()
plt.plot(sorted(data.keys()), av_comp, label="time computation")
plt.plot(sorted(data.keys()), av_comm , label="time communication")
plt.xlabel("grid size")
plt.ylabel("time(s)")
plt.legend()
plt.title("Computation vs communication")
plt.tight_layout()
plt.savefig("plots//1-4-time.png")
plt.show()