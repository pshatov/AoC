import math

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

asteroids = []

for y in range(h):
    for x in range(w):
        if lines[y][x] == "#":
            asteroids.append(Asteroid(x, y))

def calc_dxy(a, b):
    return a.x - b.x, a.y - b.y

def calc_dist2(a, b):
    dx, dy = calc_dxy(a, b)
    return dx * dx + dy * dy

def calc_tangent(a, b):
    dx, dy = calc_dxy(a, b)
    if dy == 0: return math.inf if dx > 0 else -math.inf
    else: return reduce_ratio(dx, dy)

def reduce_ratio(x, y):
    xx = x if x >= 0 else -x
    yy = y if y >= 0 else -y
    z = calc_gcd(xx, yy)
    return x // z, y // z
    
def calc_gcd(x, y):
    # y is nonzero!
    if y == 0: return x
    else: return calc_gcd(y, x % y)

max_visible = -1
for i in range(len(asteroids)):
    segs = {}
    for j in range(len(asteroids)):
        if i == j: continue
        tangent = calc_tangent(asteroids[i], asteroids[j])
        dist2 = calc_dist2(asteroids[i], asteroids[j])
        if tangent in segs.keys():
            segs[tangent].append(dist2)
        else:
            segs[tangent] = [dist2]

    num_visible = len(segs)
    if num_visible > max_visible: max_visible = num_visible
    
    print("(%d, %d): %d [max: %d]" % (asteroids[i].x, asteroids[i].y, num_visible, max_visible))
    
print("max_visible = %d" % max_visible)
        
        
