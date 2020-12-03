SLOPES = [(1, 1),
          (3, 1),
          (5, 1),
          (7, 1),
          (1, 2)]

GRID = []
with open('input.txt') as f:
    for fl in f:
        GRID.append(fl.strip())

GH = len(GRID)
GW = len(GRID[0])

m = 1
for s in SLOPES:
    sx, sy = s
    gx, gy, num_trees = 0, sy, 0
    while True:
        gx += sx
        gx_wrap = gx % GW
        if GRID[gy][gx_wrap] == '#':
            num_trees += 1
        gy += sy
        if gy >= GH:
            break
    m *= num_trees
    print("num_trees (%d, %d): %d" % (sx, sy, num_trees))
print("m: %d" % m)
