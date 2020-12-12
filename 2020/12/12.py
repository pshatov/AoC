from enum import IntEnum, auto

class Dir(IntEnum):
    East  = 0
    South = 1
    West  = 2
    North = 3

ACTIONS = []
with open('input.txt') as f:
    for fl in f:
        ACTIONS.append(fl.strip())

ship_x, ship_y, ship_dir = 0, 0, Dir.East

def turn_ship(param, direction):
    d = ship_dir
    while param > 0:
        param -= 90
        d += direction
        d %= 4
    return d
    
def move_ship(param):
    x, y = ship_x, ship_y
    if   ship_dir == Dir.East:  x += param
    elif ship_dir == Dir.South: y -= param
    elif ship_dir == Dir.West:  x -= param
    elif ship_dir == Dir.North: y += param
    return x, y

for a in ACTIONS:

    a_type, a_param = a[0], int(a[1:])
    
    if   a_type == "F": ship_x, ship_y = move_ship(a_param) 
    elif a_type == "N": ship_y += a_param
    elif a_type == "S": ship_y -= a_param
    elif a_type == "E": ship_x += a_param
    elif a_type == "W": ship_x -= a_param
    elif a_type == "R": ship_dir = turn_ship(a_param, +1)
    elif a_type == "L": ship_dir = turn_ship(a_param, -1)
    else:
        print(a_dir, a_len)
        raise RuntimeError
    
print("x: %d" % ship_x)
print("y: %d" % ship_y)
print("%d" % (abs(ship_x)+abs(ship_y)))

del ship_dir

ship_x, ship_y = 0, 0
point_dx, point_dy = 10, 1

def turn_point(param, direction):
    px, py = point_dx, point_dy
    while param > 0:
        param -= 90
        px, py = +direction * py, -direction * px
    return px, py

def move_point(param):
    return ship_x + param * point_dx, ship_y + param * point_dy
    
for a in ACTIONS:

    a_type, a_param = a[0], int(a[1:])
    
    if   a_type == "F": ship_x, ship_y = move_point(a_param) 
    elif a_type == "N": point_dy += a_param
    elif a_type == "S": point_dy -= a_param
    elif a_type == "E": point_dx += a_param
    elif a_type == "W": point_dx -= a_param
    elif a_type == "R": point_dx, point_dy = turn_point(a_param, +1)
    elif a_type == "L": point_dx, point_dy = turn_point(a_param, -1)
    else:
        print(a_dir, a_len)
        raise RuntimeError

print("x: %d" % ship_x)
print("y: %d" % ship_y)
print("%d" % (abs(ship_x)+abs(ship_y)))
