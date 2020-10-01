import os
import sys

from enum import Enum

sys.path.append(os.getcwd() + "\..")

from vt100 import vt100_cursor_off, vt100_cursor_xy

class GridLayer(Enum):
    Inner = 'Inner'
    Outer = 'Outer'

class GridPos:
    
    def __init__(self, level, layer):
        self.level = level
        self.layer = layer        
    
    def move_inside(self):
        if self.layer == GridLayer.Inner:
            self.level += 1
        self.layer = GridPos._swap_layer(self.layer)

    def move_outside(self):
        if self.layer == GridLayer.Outer:
            self.level -= 1
        self.layer = GridPos._swap_layer(self.layer)

    def _swap_layer(layer):
        if layer == GridLayer.Inner: return GridLayer.Outer
        if layer == GridLayer.Outer: return GridLayer.Inner
            
    def __eq__(self, other):
        if self.level != other.level: return False
        if self.layer != other.layer: return False
        return True
        
    def __str__(self):
        return "%d, %s" % (self.level, self.layer)
        
def load_grid(filename=None):    
    grid = []
        
    for y in range(5):
        grid.append([])
        for x in range(5):
            grid[-1].append(0)
                
    if filename is not None:
        with open(filename) as f:
            lines = f.read().splitlines()
        
        for y in range(5):
            for x in range(5):
                if lines[y][x] == '#':
                    grid[y][x] = 1

    return grid
    
def empty_grid():
    return load_grid()

grid_pos_outer = GridPos(-1, GridLayer.Inner)
grid_pos_inner = GridPos(1, GridLayer.Outer)

GRIDS_OUTER = []
GRID_MIDDLE = load_grid('input.txt')
GRIDS_INNER = []

GRIDS_OUTER_NEW = []
GRID_MIDDLE_NEW = load_grid()
GRIDS_INNER_NEW = []

def update_grids():
    for y in range(5):
        for x in range(5):
            GRID_MIDDLE[y][x] = GRID_MIDDLE_NEW[y][x]
            for z in range(len(GRIDS_OUTER)):
                GRIDS_OUTER[z][y][x] = GRIDS_OUTER_NEW[z][y][x]
            for z in range(len(GRIDS_INNER)):
                GRIDS_INNER[z][y][x] = GRIDS_INNER_NEW[z][y][x]                

def get_grid_refs(grid_pos):
    
    lvl = grid_pos.level
    alvl = lvl if lvl > 0 else -lvl
    alvl_1 = alvl - 1
    
    #print("    get_grid_refs(): lvl (alvl) == %d (%d) -> " % (lvl, alvl), end='')
    
    if lvl == 0:
        #print("MIDDLE")
        return GRID_MIDDLE, GRID_MIDDLE_NEW
    elif lvl > 0:
        if len(GRIDS_INNER) < alvl:
            #print("{created inner index %d} -> " % alvl_1, end='')
            GRIDS_INNER.append(empty_grid())
            GRIDS_INNER_NEW.append(empty_grid())
        #print("INNER[%d]" % alvl_1)
        return GRIDS_INNER[alvl_1], GRIDS_INNER_NEW[alvl_1]
    else:
        if len(GRIDS_OUTER) < alvl:
            #print("{created outer index %d} -> " % alvl_1, end='')
            GRIDS_OUTER.append(empty_grid())
            GRIDS_OUTER_NEW.append(empty_grid())
        #print("OUTER[%d]" % alvl_1)
        return GRIDS_OUTER[alvl_1], GRIDS_OUTER_NEW[alvl_1]


# (0,0) (1,0) (2,0) (3,0) (4,0)
# (0,1) (1,1) (2,1) (3,1) (4,1)
# (0,2) (1,2) (2,2) (3,2) (4,2)
# (0,3) (1,3) (2,3) (3,3) (4,3)
# (0,4) (1,4) (2,4) (3,4) (4,4)

INNER_LAYER_XY = [(1,1), (2,1), (3,1),
                  (1,2),        (3,2),
                  (1,3), (2,3), (3,3)]
                  
OUTER_LAYER_XY = [(0,0), (1,0), (2,0), (3,0), (4,0),
                  (0,1),                      (4,1),
                  (0,2),                      (4,2),
                  (0,3),                      (4,3),
                  (0,4), (1,4), (2,4), (3,4), (4,4)]

def nn(grid, x, y, layer):
    #print("+ %s @(%d, %d)" % (layer, x, y))
    return grid[y][x]
    

def num_adjacent_bugs(grid, x, y, grid_outer, grid_inner):
        
    n = 0
    
    mid = 2
    midl, midr = 1, 3
    midt, midb = 1, 3
        
    l, t = 0, 0
    r, b = 4, 4
    
    xl, xr = x-1, x+1
    yt, yb = y-1, y+1
    
    inner = 'INNER'
    current = 'CURRENT'
    outer = 'OUTER'
    
    #print("num_adjacent_bugs(): @(%d, %d)" % (x, y))
    
    if xl < 0:
        n += nn(grid_outer, midl, mid, outer)
    else:
        if xl == mid and y == mid:
            for k in range(5):
                n += nn(grid_inner, r, k, inner)
        else:
            n += nn(grid, xl, y, current)

    if xr > 4:
        n += nn(grid_outer, midr, mid, outer)
    else:
        if xr == 2 and y == mid:
            for k in range(5):
                n += nn(grid_inner, l, k, inner)
        else:
            n += nn(grid, xr, y, current)

    if yt < 0:
        n += nn(grid_outer, mid, midt, outer)
    else:
        if yt == 2 and x == mid:
            for k in range(5):
                n += nn(grid_inner, k, b, inner)
        else:
            n += nn(grid, x, yt, current)

    if yb > 4:
        n += nn(grid_outer, mid, midb, outer)
    else:
        if yb == 2 and x == mid:
            for k in range(5):
                n += nn(grid_inner, k, t, inner)
        else:
            n += nn(grid, x, yb, current)

    return n


def process_grid_pos(grid_pos):
    grid_pos_outer = GridPos(grid_pos.level, grid_pos.layer)
    grid_pos_inner = GridPos(grid_pos.level, grid_pos.layer)
    grid_pos_outer.move_outside()
    grid_pos_inner.move_inside()
    
    #print("    process_grid_pos(): %s" % grid_pos)
    
    grid, grid_new = get_grid_refs(grid_pos)
    grid_outer, _ = get_grid_refs(grid_pos_outer)
    grid_inner, _ = get_grid_refs(grid_pos_inner)
    
    #print()
    #print("    grid_outer = %s" % hex(id(grid_outer)))
    #print("    grid       = %s" % hex(id(grid)))
    #print("    grid_inner = %s" % hex(id(grid_inner)))
    #print()
    #print("    grid_new       = %s" % hex(id(grid_new)))
    #print()
    
    if grid_pos.layer == GridLayer.Inner:
        XY = INNER_LAYER_XY[:]
        
    if grid_pos.layer == GridLayer.Outer:
        XY = OUTER_LAYER_XY[:]
    
    #print("    scanning %d cells..." % len(XY))
    for xy in XY:
        x, y = xy
            
        grid_new[y][x] = grid[y][x]
            
        nab = num_adjacent_bugs(grid, x, y, grid_outer, grid_inner)

        # A bug dies (becoming an empty space) unless there is exactly one bug adjacent to it.
        if grid[y][x] and nab != 1:
            grid_new[y][x] = 0
            
        # An empty space becomes infested with a bug if exactly one or two bugs are adjacent to it.
        if not grid[y][x] and 0 < nab < 3:
            grid_new[y][x] = 1
    
            
            
    

for time in range(200):
    #
    #print("time = %d, starting grid sweep" % (time+1))
    grid_pos_current = GridPos(grid_pos_outer.level, grid_pos_outer.layer)
    #
    while True:
        #
        #print("  %s" % grid_pos_current)
        process_grid_pos(grid_pos_current)
        #
        if grid_pos_current == grid_pos_inner:
            break
        else:
            grid_pos_current.move_inside()
        #
    grid_pos_outer.move_outside()
    grid_pos_inner.move_inside()
    
    update_grids()
    #print("    grids updated.")    

def sum_bugs(grid):
    s = 0
    for y in range(5):
        for x in range(5):
            s += grid[y][x]
    return s

def print_grid(grid):
    for y in range(5):
        for x in range(5):
            if y == 2 and x == 2:
                sys.stdout.write('?')
            else:
                sys.stdout.write('#' if grid[y][x] else '.')
        sys.stdout.write('\n')
    sys.stdout.flush()

if False:
    for d in range(len(GRIDS_OUTER)):
        dd = len(GRIDS_OUTER) - d
        print("Depth %d:" % -dd)
        print_grid(GRIDS_OUTER[dd-1])
        print()

    print("Depth 0:")
    print_grid(GRID_MIDDLE)
    print()

    for d in range(len(GRIDS_INNER)):
        dd = d + 1
        print("Depth %d:" % dd)
        print_grid(GRIDS_INNER[dd-1])
        print()

bugs = 0
bugs += sum_bugs(GRID_MIDDLE)
for d in range(len(GRIDS_OUTER)):
    bugs += sum_bugs(GRIDS_OUTER[d])
for d in range(len(GRIDS_INNER)):
    bugs += sum_bugs(GRIDS_INNER[d])
    
print("bugs == %d" % bugs)
