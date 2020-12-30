from copy import deepcopy
from enum import Enum, auto


class HexSpaceDir(Enum):
    Right = auto()  # e
    Left = auto()  # w
    BottomRight = auto()  # se
    BottomLeft = auto()  # sw
    TopRight = auto()  # ne
    TopLeft = auto()  # nw


HexSpaceDirDict = {'e': HexSpaceDir.Right,
                   'w': HexSpaceDir.Left,
                   'se': HexSpaceDir.BottomRight,
                   'sw': HexSpaceDir.BottomLeft,
                   'ne': HexSpaceDir.TopRight,
                   'nw': HexSpaceDir.TopLeft}


class HexSpaceInterval:

    def __init__(self):

        self.width = 1
        self.offset = 0

    @property
    def left_edge(self):
        return -self.offset

    @property
    def right_edge(self):
        return self.width - (self.offset + 1)

    def extend_left(self):
        self.width += 1
        self.offset += 1

    def extend_right(self):
        self.width += 1


class HexSpace:

    def __init__(self):

        self.TILES = [[False]]

        self.interval_x = HexSpaceInterval()
        self.interval_y = HexSpaceInterval()

        self.x = 0
        self.y = 0

    def reset_pointer(self):
        self.x = 0
        self.y = 0

    def move_pointer(self, d):
        new_x = self.x
        new_y = self.y

        if d == HexSpaceDir.Right:
            new_x += 1
        elif d == HexSpaceDir.Left:
            new_x -= 1

        if d == HexSpaceDir.TopLeft or d == HexSpaceDir.TopRight:
            new_y += 1
        elif d == HexSpaceDir.BottomLeft or d == HexSpaceDir.BottomRight:
            new_y -= 1

        if self.y % 2 == 0:
            if d == HexSpaceDir.TopLeft or d == HexSpaceDir.BottomLeft:
                new_x -= 1
        else:
            if d == HexSpaceDir.TopRight or d == HexSpaceDir.BottomRight:
                new_x += 1

        if new_x < self.interval_x.left_edge:
            self._extend_left()
        elif new_x > self.interval_x.right_edge:
            self._extend_right()

        if new_y < self.interval_y.left_edge:
            self._extend_bottom()
        elif new_y > self.interval_y.right_edge:
            self._extend_top()

        self.x = new_x
        self.y = new_y

    def _extend_left(self):
        self.interval_x.extend_left()
        for y in range(len(self.TILES)):
            self.TILES[y].insert(0, False)

    def _extend_right(self):
        self.interval_x.extend_right()
        for y in range(len(self.TILES)):
            self.TILES[y].append(False)

    def _extend_top(self):
        self.interval_y.extend_right()
        self.TILES.append([])
        for x in range(self.interval_x.width):
            self.TILES[-1].append(False)

    def _extend_bottom(self):
        self.interval_y.extend_left()
        self.TILES.insert(0, [])
        for x in range(self.interval_x.width):
            self.TILES[0].append(False)

    @property
    def xx(self):
        return self.x + self.interval_x.offset

    @property
    def yy(self):
        return self.y + self.interval_y.offset

    def flip_tile(self):
        old_value = self.TILES[self.yy][self.xx]
        new_value = not old_value
        self.TILES[self.yy][self.xx] = new_value

    def calc_black(self):
        num = 0
        for y in range(len(self.TILES)):
            y_row = self.TILES[y]
            for x in range(len(y_row)):
                if y_row[x]: num += 1
        return num

    def extend_frame(self):
        self._extend_left()
        self._extend_right()
        self._extend_top()
        self._extend_bottom()

    def calc_adj_black(self):
        n = 0
        if self.TILES[self.yy][self.xx-1]: n += 1
        if self.TILES[self.yy][self.xx+1]: n += 1
        if self.TILES[self.yy+1][self.xx]: n += 1
        if self.TILES[self.yy-1][self.xx]: n += 1
        if self.y % 2 == 0:
            if self.TILES[self.yy+1][self.xx-1]: n += 1
            if self.TILES[self.yy-1][self.xx-1]: n += 1
        else:
            if self.TILES[self.yy+1][self.xx+1]: n += 1
            if self.TILES[self.yy-1][self.xx+1]: n += 1
        return n

    def run_mutation_step(self):
        new_tiles = deepcopy(self.TILES)
        for y in range(self.interval_y.left_edge+1, self.interval_y.right_edge):
            self.y = y
            for x in range(self.interval_x.left_edge+1, self.interval_x.right_edge):
                self.x = x
                v_old = self.TILES[self.yy][self.xx]
                v_new = v_old
                n = self.calc_adj_black()
                if v_old:
                    if n == 0 or n > 2: v_new = False
                else:
                    if n == 2: v_new = True

                new_tiles[self.yy][self.xx] = v_new
        self._swap_t_new(new_tiles)

    def _swap_t_new(self, new_tiles):
        for y in range(self.interval_y.left_edge+1, self.interval_y.right_edge):
            self.y = y
            for x in range(self.interval_x.left_edge + 1, self.interval_x.right_edge):
                self.x = x
                self.TILES[self.yy][self.xx] = new_tiles[self.yy][self.xx]


hs = HexSpace()


def load_input():
    ret = []
    with open('input.txt') as f:
        for fl in f:
            fls = fl.strip()
            ret.append(fls)
    return ret


def main():
    lines = load_input()
    process_lines(lines)
    num_black = hs.calc_black()
    print("num_black: %d" % num_black)
    hs.extend_frame()
    for i in range(100):
        hs.extend_frame()
        hs.run_mutation_step()
        print("Day %d: %d" % (i+1, hs.calc_black()))
    num_black = hs.calc_black()
    print("num_black: %d" % num_black)


def process_lines(lines):
    for i in range(len(lines)):
        next_line = lines[i]
        hs.reset_pointer()
        while next_line:
            next_dir, next_line = chew_next_line(next_line)
            hs.move_pointer(next_dir)
        hs.flip_tile()


def chew_next_line(nl):
    for d in HexSpaceDirDict:
        if nl.startswith(d):
            return HexSpaceDirDict[d], nl[len(d):]
    raise RuntimeError


if __name__ == '__main__':
    main()
