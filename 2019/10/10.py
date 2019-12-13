import math
import subprocess
import time

class Asteroid:
    
    def __init__(self, x, y):
        self._x = x
        self._y = y
    
    @property
    def x(self):
        return self._x
        
    @property
    def y(self):
        return self._y


lines = []
with open('input.txt') as f:
    for line in f:
        lines.append(line.strip())

w = len(lines[0])
h = len(lines)

bodies = []
corpses = []

for y in range(h):
    for x in range(w):
        if lines[y][x] == "#":
            bodies.append(Asteroid(x, y))

def calc_dxy(a, b):
    # x points right
    # y points down
    return b.x - a.x, a.y - b.y

def calc_dist2(a, b):
    dx, dy = calc_dxy(a, b)
    return dx * dx + dy * dy

def calc_tangent(a, b):
    dx, dy = calc_dxy(a, b)
    if dx == 0: return (math.inf, 0) if dy > 0 else (-math.inf, 0)
    else: return reduce_ratio(dx, dy)

def reduce_ratio(x, y):
    xx = x if x >= 0 else -x
    yy = y if y >= 0 else -y
    z = calc_gcd(xx, yy)
    return x // z, y // z
    
def calc_gcd(x, y):
    if y == 0: return x
    else: return calc_gcd(y, x % y)

max_visible = -1
for i in range(len(bodies)):
    segs = {}
    body_src = bodies[i]
    for j in range(len(bodies)):
        if i == j: continue
        body_dst = bodies[j]
        tangent = calc_tangent(body_src, body_dst)
        dist2 = calc_dist2(body_src, body_dst)
        dist2_body = (dist2, body_dst)
        if tangent in segs.keys():
            segs[tangent].append(dist2_body)
        else:
            segs[tangent] = [dist2_body]

    num_visible = len(segs)
    if num_visible > max_visible:
        max_visible = num_visible
        laser_index = i
        laser_segs = segs
    
    print("(%d, %d): %d [max: %d]" % (bodies[i].x, bodies[i].y, num_visible, max_visible))

laser = bodies[laser_index]
del bodies[laser_index]

print("max_visible = %d" % max_visible)
print("laser placed at target asteroid @ (%d, %d)" % (laser.x, laser.y))
input("Hit any key to continue with the second part...")
#print("\033[?25l")

field = []
for y in range(h):
    field.append(bytearray())
    for x in range(w):
        field[y] += b'.'

def map_tangent_to_dir(tangent):
    
    # laser_dir == 0: up         (dx = 0, dy > 0) +inf
    # laser_dir == 1: up-right   (dx > 0, dy > 0)
    # laser_dir == 2: right      (dx > 0, dy = 0)
    # laser_dir == 3: down-right (dx > 0, dy < 0)
    # laser_dir == 4: down       (dx = 0, dy < 0) -inf
    # laser_dir == 5: down-left  (dx < 0, dy < 0)
    # laser_dir == 6: left       (dx < 0, dy = 0)
    # laser_dir == 7: up-left    (dx < 0, dy > 0)

    dx = tangent[0]
    dy = tangent[1]

    if   dx ==  math.inf: return 0
    elif dx == -math.inf: return 4
    
    if dx > 0:
        if   dy > 0: return 1
        elif dy < 0: return 3
        else:        return 2
    else:
        if   dy > 0: return 7
        elif dy < 0: return 5
        else:        return 6
    
def draw_field(field, width, height, targets, laser, corpses=None, quick_update=False):
    print("\033[?25l\033[0;0H")
    if quick_update:
        for y in range(height+1):
            print("", flush=False)
        return
    
    for y in range(height):
        for x in range(width):
            field[y][x] = ord('.')
        
    field[laser.y][laser.x] = ord('X')

    for target in targets:
        field[target.y][target.x] = ord('#')

    if corpses is not None:
        for corpse in corpses:
            field[corpse.y][corpse.x] = ord('@')

    for y in range(height):
        print(field[y].decode().replace("@", "\033[31m@\033[0m"), flush=False)
        
    print("")

def compare_tangents_lt(a, b):
    return (a[1]/a[0]) > (b[1]/b[0])

def compare_tangents_le(a, b):
    return (a[1]/a[0]) >= (b[1]/b[0])

def find_smallest_tangent(tangents):
    if len(tangents) == 0: return None
    min_tangent = None
    for next_tangent in tangents:
        if min_tangent is None: min_tangent = next_tangent
        elif compare_tangents_lt(next_tangent, min_tangent): min_tangent = next_tangent

    return min_tangent

def find_larger_tangent(tangents, thres_tangent):
    if len(tangents) == 0: return None
    min_tangent = None
    for next_tangent in tangents:
        if compare_tangents_le(next_tangent, thres_tangent): continue
        if min_tangent is None: min_tangent = next_tangent
        elif compare_tangents_lt(next_tangent, min_tangent): min_tangent = next_tangent

    return min_tangent
    
def find_smallest_distance(segs):
    min_dist = None
    target = None
    for seg in segs:
        if min_dist is None: min_dist, target = seg[0], seg
        elif seg[0] < min_dist: min_dist, target = seg[0], seg
    return target

def step_dir(dir):
    return (dir + 1) % 8

def unity_tangent(dir):
    if dir   == 0: return (math.inf,   0)
    elif dir == 1: return (1,          1)
    elif dir == 2: return (1,          0)
    elif dir == 3: return (1,         -1)
    elif dir == 4: return (-math.inf,  0)
    elif dir == 5: return (-1,        -1)
    elif dir == 6: return (-1,         0)
    elif dir == 7: return (-1,         1)

def laser_find_next_target(segs, laser, next_dir, prev_tangent):
        
    next_dir_same = next_dir
    next_dir_next = step_dir(next_dir)
    
    prev_dir = map_tangent_to_dir(prev_tangent)
    
    if prev_dir != next_dir:

        # next direction, need to find smallest tangent
        
        next_tangent = find_smallest_tangent(segs.keys())
        if next_tangent is None: return next_dir_next, unity_tangent(next_dir), None
        
        next_target = find_smallest_distance(segs[next_tangent])
        if (next_dir % 2) == 0: return next_dir_next, next_tangent, next_target
        else:                   return next_dir_same, next_tangent, next_target

    else:
    
        # same direction, need to find next tangent        
        
        next_tangent = find_larger_tangent(segs.keys(), prev_tangent)
        if next_tangent is None: return next_dir_next, unity_tangent(next_dir), None
        
        next_target = find_smallest_distance(segs[next_tangent])
        return next_dir_same, next_tangent, next_target
        
                        
subprocess.run(["clear"])
draw_field(field, w, h, bodies, laser)

bodies_per_sec = 25
sec_per_body = 1.0 / bodies_per_sec

laser_segs_dir = []
for dir in range(8):
    laser_segs_dir.append({})
    
for tangent in laser_segs.keys():
    dir = map_tangent_to_dir(tangent)
    laser_segs_dir[dir][tangent] = laser_segs[tangent]

cur_dir = 0
prev_tangent = unity_tangent(7)

missed_in_a_row = 0

while len(bodies) > 0:
    t0 = time.time()
    next_dir, next_tangent, target = laser_find_next_target(laser_segs_dir[cur_dir], laser, cur_dir, prev_tangent)
    if not target is None:
        corpses.append(target[1])
        bodies.remove(target[1])
        laser_segs_dir[cur_dir][next_tangent].remove(target)
        if len(laser_segs_dir[cur_dir][next_tangent]) == 0:
            del laser_segs_dir[cur_dir][next_tangent]
        draw_field(field, w, h, bodies, laser, corpses)
        t1 = time.time()
        dt = t1 - t0
        dt_rem = sec_per_body - dt
        if dt_rem > 0:
            time.sleep(dt_rem)
    else:
        draw_field(field, w, h, bodies, laser, corpses, quick_update=True)
    
    print("kills: %d" % len(corpses))
    if len(corpses) == 200:
        print("200th asteroid destroyed @ (%d, %d)" % (target[1].x, target[1].y))
    
    cur_dir = next_dir
    prev_tangent = next_tangent


