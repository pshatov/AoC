import copy

NUM_CYCLES = 6

class Pocket:

    def __init__(self, dx, dy):
        #
        self._z_max = 0
        self._y_max = dy-1
        self._x_max = dx-1
        #
        self._P = []
        self._P.append([])
        #
        for y in range(dy):
            self._P[-1].append([])
            for x in range(dx):
                self._P[-1][-1].append('.')

    @property
    def z_max(self): return self._z_max

    @property
    def y_max(self): return self._y_max

    @property
    def x_max(self): return self._x_max

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


def load_input(filename='input.txt'):
    P = []
    with open(filename) as f:
        for fl in f:
            fls = fl.strip()
            P.append([])
            for flsi in fls:
                P[-1].append(flsi)
    return P


def boot_cycle(p):
    p.extend_xyz()
    p.branch()
    for z in p.z_range_inner:
        for y in p.y_range_inner:
            for x in p.x_range_inner:
                cube = p.get_cube(x, y, z)
                num_adj = p.calc_adj_cubes(x, y, z)

                if cube == '#':
                    if num_adj == 2 or num_adj == 3: cube_new = '#'
                    else: cube_new = '.'
                else:
                    if num_adj == 3: cube_new = '#'
                    else: cube_new = '.'

                p.set_branch(x, y, z, cube_new)


    p.merge()


def main():
    P = load_input()
    pocket = Pocket(len(P[0]), len(P))
    for y in range(0, len(P[0])):
        for x in range(0, len(P)):
            pocket.set_cube(x, y, 0, P[y][x])

    pocket.extend_xyz()

    pocket.print_pocket(1)

    for n in range(NUM_CYCLES):
        boot_cycle(pocket)

    num_active = 0
    for z in pocket.z_range_inner:
        for y in pocket.y_range_inner:
            for x in pocket.x_range_inner:
                if pocket.get_cube(x, y, z) == '#':
                    num_active += 1
    print("num_active: %d" % num_active)

if __name__ == '__main__':
    main()