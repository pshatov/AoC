import sys
import keyboard

GRID = []
NEW_GRID = []
STATES = []

def _vt100_cursor_off():
    sys.stdout.write("\033[?25l")

def _vt100_cursor_xy(x, y):
    sys.stdout.write("\033[%d;%dH" % (y+1, x+1))

def wait_key():
    done = False
    while not done:
        k = keyboard.read_event(suppress=True)
        if k.name == 'q' and k.event_type == "down": sys.exit()
        done = k.name == 'space' and k.event_type == "down"    

def draw_grid():
    for y in range(5):
        for x in range(5):
            sys.stdout.write('#' if GRID[y][x] else '.')
        sys.stdout.write('\n')
    sys.stdout.flush()

def num_adjacent_bugs(x, y):
    n = 0
    if y < 4: n += GRID[y+1][x]
    if x < 4: n += GRID[y][x+1]
    if y > 0: n += GRID[y-1][x]
    if x > 0: n += GRID[y][x-1]
    return n

def grid_index():
    pwr = 0
    index = 0
    for y in range(5):
        for x in range(5):
            index |= (GRID[y][x] << pwr)
            pwr += 1
    return index

def mutate_grid():

    for y in range(5):
        for x in range(5):

            NEW_GRID[y][x] = GRID[y][x]

            nab = num_adjacent_bugs(x, y)

            # A bug dies (becoming an empty space) unless there is exactly one bug adjacent to it.
            if GRID[y][x] and nab != 1:
                NEW_GRID[y][x] = 0
            
            # An empty space becomes infested with a bug if exactly one or two bugs are adjacent to it.
            if not GRID[y][x] and 0 < nab < 3:
                NEW_GRID[y][x] = 1
            
    for y in range(5):
        for x in range(5):
            GRID[y][x] = NEW_GRID[y][x]

_vt100_cursor_off()

with open('input.txt') as f:
    lines = f.read().splitlines()

for y in range(5):
    GRID.append([])
    NEW_GRID.append([])
    for x in range(5):
        GRID[-1].append(0)
        NEW_GRID[-1].append(0)

for y in range(5):
    for x in range(5):
        if lines[y][x] == '#':
            GRID[y][x] = 1

for y in range(2 ** 25):
    STATES.append(0)

steps = 0
while True:
    index = grid_index()
    _vt100_cursor_xy(0, 0)
    print("steps = %d, index = %s (%d)" % (steps, bin(index), index))
    draw_grid()
    STATES[index] += 1
    if STATES[index] > 1:
        print(">>> ...")
        break
    
    steps += 1
    mutate_grid()
    
wait_key()
        
