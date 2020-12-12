from enum import IntEnum, auto

class Dir(IntEnum):
    East  = 0
    South = 1
    West  = 2
    North = 3

DIR_STR = {Dir.East:  "East",
           Dir.South: "South",
           Dir.West:  "West",
           Dir.North: "North"}

ACTIONS = []
with open('input.txt') as f:
    for fl in f:
        ACTIONS.append(fl.strip())

ship_x, ship_y, ship_dir = 0, 0, Dir.East

def turn(param, direction):
    d = ship_dir
    while param > 0:
        param -= 90
        d += direction
        d %= 4
    return d
    
def move(param):
    x, y = ship_x, ship_y
    if   ship_dir == Dir.East:  x += param
    elif ship_dir == Dir.South: y -= param
    elif ship_dir == Dir.West:  x -= param
    elif ship_dir == Dir.North: y += param
    return x, y

for a in ACTIONS:

    a_type, a_param = a[0], int(a[1:])
    #print("ACTION: '%s', %d" % (a_type, a_param))
    
    if   a_type == "F": ship_x, ship_y = move(a_param) 
    
    elif a_type == "N":
        #print("  Y += %d" % a_param)
        ship_y += a_param
    
    elif a_type == "S":
        #print("  Y -= %d" % a_param)
        ship_y -= a_param
        
    elif a_type == "E":
        #print("  X += %d" % a_param)
        ship_x += a_param
        
    elif a_type == "W":
        #print("  X -= %d" % a_param)
        ship_x -= a_param
        
    elif a_type == "R":
        ship_dir = turn(a_param, +1)
        
    elif a_type == "L":
        ship_dir = turn(a_param, -1)
        
    else:
        #print(a_dir, a_len)
        raise RuntimeError
        
    #print("    (%d, %d, %s)" % (ship_x, ship_y, DIR_STR[ship_dir]))
    
print("x: %d" % ship_x)
print("y: %d" % ship_y)
print("%d" % (abs(ship_x)+abs(ship_y)))
