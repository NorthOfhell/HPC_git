filename = "output"
all_lines = []

# Read all lines
for i in range(6):
    with open(f"{filename}{i}.dat", "r") as infile:
        for line in infile:
            parts = line.strip().split()
            if len(parts) == 3:
                x, y, val = parts
                all_lines.append((int(x), int(y), val))

# Sort by x then y
all_lines.sort(key=lambda t: (t[0], t[1]))

# Write sorted lines
with open("combined_output.dat", "w") as outfile:
    for x, y, val in all_lines:
        outfile.write(f"{x} {y} {val}\n")