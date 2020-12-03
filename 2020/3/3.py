GRID = []
with open('input.txt') as f:
    for fl in f:
        GRID.append(fl.strip())

GH = len(GRID)
GW = len(GRID[0])

gx, num_trees = 0, 0
for gy in range(1, GH):
    gx += 3
    gx_wrap = gx % GW
    if GRID[gy][gx_wrap] == '#':
        num_trees += 1

print("num_trees: %d" % num_trees)
