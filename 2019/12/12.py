import re
import math
num_moons = 4

class Moon:
    
    _scan_regexp = "^\<x\=(\-?\d+)\,\sy\=(\-?\d+),\sz\=(\-?\d+)\>$"
    
    def __init__(self, str):
        self._x, self._y, self._z = self._parse_scan(str)
        
        self._vx = 0
        self._vy = 0
        self._vz = 0
        
    def _parse_scan(self, scan):
        m = re.fullmatch(self._scan_regexp, scan)
        if m is None: raise Exception("Can't parse scan line '%s'!" % (scan))
        return int(m.group(1)), int(m.group(2)), int(m.group(3))

    def apply_gravity(self, other_moon):
        if   other_moon.x > self._x: self._vx += 1
        elif other_moon.x < self._x: self._vx -= 1
        
        if   other_moon.y > self._y: self._vy += 1
        elif other_moon.y < self._y: self._vy -= 1

        if   other_moon.z > self._z: self._vz += 1
        elif other_moon.z < self._z: self._vz -= 1
        
    def apply_velocity(self):
        self._x += self._vx
        self._y += self._vy
        self._z += self._vz
        
    def print_state(self):
        print("pos=<x=%d, y=%d, z=%d>, vel=<x=%d, y=%d, z=%d>" % (self._x, self._y, self._z, self._vx, self._vy, self._vz))
    
    @property
    def total_energy(self):
        pot = 0
        pot += int(math.fabs(self._x))
        pot += int(math.fabs(self._y))
        pot += int(math.fabs(self._z))
        kin = 0
        kin += int(math.fabs(self._vx))
        kin += int(math.fabs(self._vy))
        kin += int(math.fabs(self._vz))
        return pot * kin
    
    @property
    def x(self):
        return self._x
        
    @property
    def y(self):
        return self._y

    @property
    def z(self):
        return self._z
        
    @property
    def state_x(self):
        return (self._x, self._vx)

    @property
    def state_y(self):
        return (self._y, self._vy)

    @property
    def state_z(self):
        return (self._z, self._vz)

moons = []
with open('input.txt') as f:
    for i in range(num_moons):
        moons.append(Moon(f.readline().strip()))

moons1 = moons.copy()
moons2 = moons.copy()

for k in range(1000):

    for i in range(num_moons):
        for j in range(num_moons):
            if i == j: continue
            moons1[i].apply_gravity(moons1[j])

    for i in range(num_moons):
        moons1[i].apply_velocity()
            
#    print("\nAfter %d step%s:" % (k+1, "s" if k > 0 else ""))
#    for i in range(num_moons):
#        moons1[i].print_state()
        
    total_energy = 0
    for i in range(num_moons):
        total_energy += moons1[i].total_energy
        
    #print("\ntotal_energy = %d" % (total_energy))
    
print("\ntotal_energy = %d" % (total_energy))


# def all_states_x():
    # all_states = []
    # for i in range(num_moons):
        # all_states.append(moons2[i].state_x)
    # return all_states

# def all_states_y():
    # all_states = []
    # for i in range(num_moons):
        # all_states.append(moons2[i].state_y)
    # return all_states

# def all_states_z():
    # all_states = []
    # for i in range(num_moons):
        # all_states.append(moons2[i].state_z)
    # return all_states

# num_steps = 0

# period_x = -1
# period_y = -1
# period_z = -1

# prev_states_x = []
# prev_states_y = []
# prev_states_z = []

# prev_states_x.append(all_states_x())
# prev_states_y.append(all_states_y())
# prev_states_z.append(all_states_z())

# def matches_previous_x():
    # x = all_states_x()
    # for prev_x in prev_states_x:
        # if x == prev_x:
            # print(prev_x)
            # return True
    # return False

# def matches_previous_y():
    # y = all_states_y()
    # for prev_y in prev_states_y:
        # if y == prev_y:
            # print(prev_y)
            # return True
    # return False

# def matches_previous_z():
    # z = all_states_z()
    # for prev_z in prev_states_z:
        # if z == prev_z:
            # print(prev_z)
            # return True
    # return False

# for k in range(100000):

    # num_steps += 1

    # if (num_steps % 1000) == 0:
        # print("num_steps = %d" % num_steps)

    # for i in range(num_moons):
        # for j in range(num_moons):
            # if i == j: continue
            # moons2[i].apply_gravity(moons2[j])

    # for i in range(num_moons):
        # moons2[i].apply_velocity()
        
    # if period_x < 0:
        # if matches_previous_x():
            # print("Found X!")
            # period_x = num_steps

# #    if period_y < 0:
# #        if matches_previous_y():
# #            print("Found Y!")
# #            period_y = num_steps

# #    if period_z < 0:
# #        if matches_previous_z():
# #            print("Found Z!")
# #            period_z = num_steps
        
    # prev_states_x.append(all_states_x())
# #    prev_states_y.append(all_states_y())
# #    prev_states_z.append(all_states_z())
    
# print("period_x = %d" % period_x)
# print("period_y = %d" % period_y)
# print("period_z = %d" % period_z)

# def calc_gcd(x, y):
    # if y == 0: return x
    # else: return calc_gcd(y, x % y)

# period_xy = period_x * period_y // calc_gcd(period_x, period_y)
# period_xyz = period_xy * period_z // calc_gcd(period_xy, period_z)

# print("period_xyz = %d" % period_xyz)

