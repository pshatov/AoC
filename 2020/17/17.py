import copy

NUM_CYCLES = 6

class Pocket3D:

    def __init__(self, dx, dy):
        #
        self._z_max = 0
        self._y_max = dy-1
        self._x_max = dx-1
        #
        self._P = [] # list of XY layers
        self._P.append([]) # XY layer Z=0
        #
        for y in range(dy):
            self._P[-1].append([])
            for x in range(dx):
                self._P[-1][-1].append('.')

    @property
    def z_range(self): return range(self._z_max+1)

    @property
    def y_range(self): return range(self._y_max+1)

    @property
    def x_range(self): return range(self._x_max+1)

    @property
    def z_range_inner(self): return range(1, self._z_max)

    @property
    def y_range_inner(self): return range(1, self._y_max)

    @property
    def x_range_inner(self): return range(1, self._x_max)

    def calc_adj_cubes(self, x, y, z):
        n = 0
        for zz in range(z-1,z+2):
            for yy in range(y-1, y+2):
                for xx in range(x-1, x+2):
                    if zz == z and yy == y and xx == x: continue
                    if self._P[zz][yy][xx] == '#': n += 1
        return n

    def get_cube(self, x, y, z):
        return self._P[z][y][x]

    def set_cube(self, x, y, z, v):
        self._P[z][y][x] = v

    def set_branch(self, x, y, z, v):
        self._T[z][y][x] = v

    def _extend_x(self):
        for z in self.z_range:
            for y in self.y_range:
                self._P[z][y].insert(0, '.')
                self._P[z][y].append('.')
        self._x_max += 2

    def _extend_y(self):
        for z in self.z_range:
            self._P[z].insert(0, [])
            self._P[z].append([])
            for x in self.x_range:
                self._P[z][0].append('.')
                self._P[z][-1].append('.')
        self._y_max += 2

    def _extend_z(self):
        self._P.insert(0, [])
        self._P.append([])
        for y in self.y_range:
            self._P[0].append([])
            self._P[-1].append([])
            for x in self.x_range:
                self._P[0][-1].append('.')
                self._P[-1][-1].append('.')
        self._z_max += 2

    def extend_xyz(self):
        self._extend_x()
        self._extend_y()
        self._extend_z()

    def print_pocket(self, z=0):
        for y in self.y_range:
            for x in self.x_range:
                print(self._P[z][y][x], end='')
            print()
        print()

    def branch(self):
        self._T = copy.deepcopy(self._P)

    def merge(self):
        for z in self.z_range_inner:
            for y in self.y_range_inner:
                for x in self.x_range_inner:
                    self._P[z][y][x] = self._T[z][y][x]

class Pocket4D:

    def __init__(self, dx, dy):
        #
        self._w_max = 0
        self._z_max = 0
        self._y_max = dy-1
        self._x_max = dx-1
        #
        self._P = [] # list of XYZ cubes
        self._P.append([]) # XYZ cube W=0
        self._P[-1].append([]) # list of XY planes Z = 0
        #
        for y in range(dy):
            self._P[-1][-1].append([])
            for x in range(dx):
                self._P[-1][-1][-1].append('.')

    @property
    def w_range(self): return range(self._w_max+1)

    @property
    def z_range(self): return range(self._z_max+1)

    @property
    def y_range(self): return range(self._y_max+1)

    @property
    def x_range(self): return range(self._x_max+1)

    @property
    def w_range_inner(self): return range(1, self._w_max)

    @property
    def z_range_inner(self): return range(1, self._z_max)

    @property
    def y_range_inner(self): return range(1, self._y_max)

    @property
    def x_range_inner(self): return range(1, self._x_max)

    def calc_adj_cubes(self, x, y, z, w):
        n = 0
        for ww in range(w-1, w+2):
            for zz in range(z-1,z+2):
                for yy in range(y-1, y+2):
                    for xx in range(x-1, x+2):
                        if ww == w and zz == z and yy == y and xx == x: continue
                        if self._P[ww][zz][yy][xx] == '#': n += 1
        return n

    def get_cube(self, x, y, z, w):
        return self._P[w][z][y][x]

    def set_cube(self, x, y, z, w, v):
        self._P[w][z][y][x] = v

    def set_branch(self, x, y, z, w, v):
        self._T[w][z][y][x] = v

    def _extend_x(self):
        for w in self.w_range:
            for z in self.z_range:
                for y in self.y_range:
                    self._P[w][z][y].insert(0, '.')
                    self._P[w][z][y].append('.')
        self._x_max += 2

    def _extend_y(self):
        for w in self.w_range:
            for z in self.z_range:
                self._P[w][z].insert(0, [])
                self._P[w][z].append([])
                for x in self.x_range:
                    self._P[w][z][0].append('.')
                    self._P[w][z][-1].append('.')
        self._y_max += 2

    def _extend_z(self):
        for w in self.w_range:
            self._P[w].insert(0, [])
            self._P[w].append([])
            for y in self.y_range:
                self._P[w][0].append([])
                self._P[w][-1].append([])
                for x in self.x_range:
                    self._P[w][0][-1].append('.')
                    self._P[w][-1][-1].append('.')
        self._z_max += 2

    def _extend_w(self):
        self._P.insert(0, [])
        self._P.append([])
        for z in self.z_range:
            self._P[0].append([])
            self._P[-1].append([])
            for y in self.y_range:
                self._P[0][-1].append([])
                self._P[-1][-1].append([])
                for x in self.x_range:
                    self._P[0][-1][-1].append('.')
                    self._P[-1][-1][-1].append('.')
        self._w_max += 2

    def extend_xyzw(self):
        self._extend_x()
        self._extend_y()
        self._extend_z()
        self._extend_w()

    def print_pocket(self, z=0):
        for y in self.y_range:
            for x in self.x_range:
                print(self._P[z][y][x], end='')
            print()
        print()

    def branch(self):
        self._T = copy.deepcopy(self._P)

    def merge(self):
        for w in self.w_range_inner:
            for z in self.z_range_inner:
                for y in self.y_range_inner:
                    for x in self.x_range_inner:
                        self._P[w][z][y][x] = self._T[w][z][y][x]

def load_input(filename='input.txt'):
    P = []
    with open(filename) as f:
        for fl in f:
            fls = fl.strip()
            P.append([])
            for flsi in fls:
                P[-1].append(flsi)
    return P


def calc_cube(c, n):
    if c == '#':
        if n == 2 or n == 3: return '#'
        else: return '.'
    else:
        if n == 3: return '#'
        else: return '.'


def boot_cycle_3d(p):
    p.extend_xyz()
    p.branch()
    for z in p.z_range_inner:
        for y in p.y_range_inner:
            for x in p.x_range_inner:
                cube = p.get_cube(x, y, z)
                num_adj = p.calc_adj_cubes(x, y, z)
                cube_new = calc_cube(cube, num_adj)
                p.set_branch(x, y, z, cube_new)
    p.merge()

def boot_cycle_4d(p):
    p.extend_xyzw()
    p.branch()
    for w in p.w_range_inner:
        for z in p.z_range_inner:
            for y in p.y_range_inner:
                for x in p.x_range_inner:
                    cube = p.get_cube(x, y, z, w)
                    num_adj = p.calc_adj_cubes(x, y, z, w)
                    cube_new = calc_cube(cube, num_adj)
                    p.set_branch(x, y, z, w, cube_new)
    p.merge()


def main():
    P = load_input()
    pocket_3d = Pocket3D(len(P[0]), len(P))
    pocket_4d = Pocket4D(len(P[0]), len(P))
    for y in range(0, len(P[0])):
        for x in range(0, len(P)):
            pocket_3d.set_cube(x, y, 0, P[y][x])
            pocket_4d.set_cube(x, y, 0, 0, P[y][x])

    pocket_3d.extend_xyz()
    pocket_4d.extend_xyzw()

    for n in range(NUM_CYCLES):
        boot_cycle_3d(pocket_3d)
        boot_cycle_4d(pocket_4d)

    num_active_3d = 0
    num_active_4d = 0

    for z in pocket_3d.z_range_inner:
        for y in pocket_3d.y_range_inner:
            for x in pocket_3d.x_range_inner:
                if pocket_3d.get_cube(x, y, z) == '#':
                    num_active_3d += 1

    for w in pocket_4d.w_range_inner:
        for z in pocket_4d.z_range_inner:
            for y in pocket_4d.y_range_inner:
                for x in pocket_4d.x_range_inner:
                    if pocket_4d.get_cube(x, y, z, w) == '#':
                        num_active_4d += 1


    print("num_active_3d: %d" % num_active_3d)
    print("num_active_4d: %d" % num_active_4d)


if __name__ == '__main__':
    main()