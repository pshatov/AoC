import sys
import copy
from enum import Enum, IntEnum, auto

TILES = {}
EDGE_MARKS = {}
CORNER_TILES = {}
SIDE_TILES = {}

FIXED_CORNER_TILES = []
FIXED_SIDE_TILES = []
FIXED_CENTER_TILES = []

S = 10  # tile side
N = 12  # map side

MONSTER = ['                  # ',
           '#    ##    ##    ###',
           ' #  #  #  #  #  #   ']

class TileCorner(IntEnum):
    TopLeft = 0
    TopRight = 1
    BottomRight = 2
    BottomLeft = 3


class TileSide(IntEnum):
    Top = 0
    Right = 1
    Bottom = 2
    Left = 3


class TileEdge(Enum):
    Top = auto()
    Bottom = auto()
    Left = auto()
    Right = auto()


class Tile:

    def __init__(self):
        self._T = []
        self._Z = None

    def preallocate(self):
        self._Z = copy.deepcopy(self._T)

    def append_input_row(self, r):
        self._T.append([])
        for i in range(len(r)):
            self._T[-1].append(r[i])

    def edge_mark(self, e):
        m = ""
        for xy in range(S):
            if e == TileEdge.Top: m += self._T[0][xy]
            elif e == TileEdge.Bottom: m += self._T[-1][xy]
            elif e == TileEdge.Left: m += self._T[xy][0]
            elif e == TileEdge.Right: m += self._T[xy][-1]
        return m

    def rotate(self):
        for y in range(S):
            for x in range(S):
                self._Z[x][-(y+1)] = self._T[y][x]
        self._zt()

    def mirror(self):
        for y in range(S):
            for x in range(S):
                self._Z[y][-(x+1)] = self._T[y][x]
        self._zt()

    def _zt(self):
        for y in range(S):
            for x in range(S):
                self._T[y][x] = self._Z[y][x]

    def align_to_other_edge(self, other_tile, other_tile_edge):
        for i in range(4):
            if self.try_align_to_other_edge_worker(other_tile, other_tile_edge): return
            self.rotate()
        self.mirror()
        for i in range(4):
            if self.try_align_to_other_edge_worker(other_tile, other_tile_edge): return
            self.rotate()
        raise RuntimeError

    def try_align_to_other_edge_worker(self, other_tile, other_tile_edge):
        mark = other_tile.edge_mark(other_tile_edge)
        if other_tile_edge == TileEdge.Top and self.edge_mark(TileEdge.Bottom) == mark: return True
        elif other_tile_edge == TileEdge.Bottom and self.edge_mark(TileEdge.Top) == mark: return True
        elif other_tile_edge == TileEdge.Left and self.edge_mark(TileEdge.Right) == mark: return True
        elif other_tile_edge == TileEdge.Right and self.edge_mark(TileEdge.Left) == mark: return True
        return False

    def find_matching_tile_id(self, my_edge, other_tile_list):
        my_edge_mark = self.edge_mark(my_edge)
        my_edge_mark_rev = my_edge_mark[::-1]
        for other_tile_key in other_tile_list:
            other_tile = other_tile_list[other_tile_key]
            for e in TileEdge:
                e_mark = other_tile.edge_mark(e)
                if e_mark == my_edge_mark or e_mark == my_edge_mark_rev:
                    return other_tile_key
        return -1

    def ch(self, x, y):
        return self._T[y][x]

    def ch_mid(self, y):
        ch = ""
        for x in range(1, S-1):
            ch += self._T[y][x]
        return ch
        
def load_tiles():
    with open('input.txt') as f:
        f_lines = f.readlines()

    for li in range(0, len(f_lines), 12):
        ls = f_lines[li].strip()
        tile_id = int(ls.split(' ')[1][:-1])
        t = Tile()
        for j in range(1, 11):
            ls = f_lines[li+j].strip()
            t.append_input_row(ls)
        t.preallocate()
        TILES[tile_id] = t


def scan_edge_marks_worker(edge_mark):
    edge_mark_rev = edge_mark[::-1]
    if edge_mark in EDGE_MARKS.keys(): EDGE_MARKS[edge_mark] += 1
    elif edge_mark_rev in EDGE_MARKS.keys(): EDGE_MARKS[edge_mark_rev] += 1
    else: EDGE_MARKS[edge_mark] = 1


def scan_edge_marks():
    for tile in TILES.values():
        for e in TileEdge:
            e_mark = tile.edge_mark(e)
            scan_edge_marks_worker(e_mark)


def check_corner_or_edge_tile_worker(edge_mark):
    edge_mark_rev = edge_mark[::-1]
    if edge_mark in EDGE_MARKS and EDGE_MARKS[edge_mark] == 1: return True
    elif edge_mark_rev in EDGE_MARKS and EDGE_MARKS[edge_mark_rev] == 1: return True
    else: return False


def find_corner_and_side_tiles():
    for tile_id in TILES.keys():
        tile = TILES[tile_id]
        n = 0
        for e in TileEdge:
            e_mark = tile.edge_mark(e)
            if check_corner_or_edge_tile_worker(e_mark): n += 1
        if n == 2: CORNER_TILES[tile_id] = tile
        if n == 1: SIDE_TILES[tile_id] = tile
    for corner_tile_id in CORNER_TILES.keys():
        del TILES[corner_tile_id]
    for side_tile_id in SIDE_TILES.keys():
        del TILES[side_tile_id]


def start_assembly():
    for i in range(4):
        FIXED_CORNER_TILES.append(None)
        FIXED_SIDE_TILES.append([])
        for j in range(N-2):
            FIXED_SIDE_TILES[i].append(None)

    for j in range(N-2):
        FIXED_CENTER_TILES.append([])
        for k in range(N-2):
            FIXED_CENTER_TILES[j].append(None)


def assemble_frame():

    corner_matching_edge, side_matching_edge = None, TileEdge.Right
    for phase in range(4):

        if phase == 0: pass
        elif phase == 1: corner_matching_edge, side_matching_edge = TileEdge.Right, TileEdge.Bottom
        elif phase == 2: corner_matching_edge, side_matching_edge = TileEdge.Bottom, TileEdge.Left
        elif phase == 3: corner_matching_edge, side_matching_edge = TileEdge.Left, TileEdge.Top

        # find corner tile
        if phase == 0:
            corner_tile_id_next = list(CORNER_TILES.keys())[0]
        else:
            corner_tile_id_next = FIXED_SIDE_TILES[phase-1][-1].find_matching_tile_id(corner_matching_edge,
                                                                                      CORNER_TILES)

        # store tile
        corner_tile_next = CORNER_TILES[corner_tile_id_next]

        # align as needed
        if phase == 0:
            while corner_tile_next.find_matching_tile_id(TileEdge.Left, SIDE_TILES) > 0: corner_tile_next.rotate()
            while corner_tile_next.find_matching_tile_id(TileEdge.Top, SIDE_TILES) > 0: corner_tile_next.rotate()
        else:
            corner_tile_next.align_to_other_edge(FIXED_SIDE_TILES[phase-1][-1], corner_matching_edge)

        # move
        FIXED_CORNER_TILES[phase] = corner_tile_next
        del CORNER_TILES[corner_tile_id_next]

        # top side
        side_tile_prev = FIXED_CORNER_TILES[phase]
        for i in range(N-2):
            side_tile_id_next = side_tile_prev.find_matching_tile_id(side_matching_edge, SIDE_TILES)
            side_tile_next = SIDE_TILES[side_tile_id_next]
            side_tile_next.align_to_other_edge(side_tile_prev, side_matching_edge)
            FIXED_SIDE_TILES[phase][i] = side_tile_next
            del SIDE_TILES[side_tile_id_next]
            side_tile_prev = side_tile_next


def assemble_center():

    for y in range(N-2):
        for x in range(N-2):
            center_tile_prev = FIXED_SIDE_TILES[TileSide.Left][-(y+1)] if x == 0 else FIXED_CENTER_TILES[y][x-1]
            center_tile_id_next = center_tile_prev.find_matching_tile_id(TileEdge.Right, TILES)
            center_tile_next = TILES[center_tile_id_next]
            center_tile_next.align_to_other_edge(center_tile_prev, TileEdge.Right)
            FIXED_CENTER_TILES[y][x] = center_tile_next
            del TILES[center_tile_id_next]


def dump_tile_table_separator():
    for tx in range(N):
        pl = tx == 0
        if pl: sys.stdout.write('+')
        sys.stdout.write("%s+" % (10 * '-'))
    sys.stdout.write("\n")


def dump_tile_row(t, r, pl=False, pr=False):
    if pl: sys.stdout.write('|')

    for x in range(S):
        sys.stdout.write(t.ch(x, r) if t is not None else 'x')

    if pr: sys.stdout.write('|')


def dump_entire_table():
    for ty in range(N):
        if ty == 0: dump_tile_table_separator()
        for y in range(S):
            for tx in range(N):

                pl = tx == 0
                pr = True

                # top row
                if ty == 0:
                    if tx == 0: t = FIXED_CORNER_TILES[TileCorner.TopLeft]  # top-left
                    elif tx == N - 1: t = FIXED_CORNER_TILES[TileCorner.TopRight]  # top-right
                    else: t = FIXED_SIDE_TILES[TileSide.Top][tx - 1]  # top side

                # bottom row
                elif ty == N - 1:
                    if tx == N - 1: t = FIXED_CORNER_TILES[TileCorner.BottomRight]  # bottom-right
                    elif tx == 0: t = FIXED_CORNER_TILES[TileCorner.BottomLeft]  # bottom-left
                    else: t = FIXED_SIDE_TILES[TileSide.Bottom][N - (tx + 2)]  # bottom side

                # middle rows
                else:
                    if tx == N - 1: t = FIXED_SIDE_TILES[TileSide.Right][ty - 1]  # right side
                    elif tx == 0: t = FIXED_SIDE_TILES[TileSide.Left][N - (ty + 2)]  # left side
                    else: t = FIXED_CENTER_TILES[ty-1][tx-1]

                dump_tile_row(t, y, pl=pl, pr=pr)

            sys.stdout.write("\n")

        dump_tile_table_separator()


def dump_corner_ids():
    if len(CORNER_TILES) != 4: raise RuntimeError
    m = 1
    for z in CORNER_TILES.keys():
        m *= z
    print("m: %d" % m)


def dump_sea(s):
    for y in range(len(s)):
        sys.stdout.write("%s\n" % s[y])
    sys.stdout.write("\n")


def compress_sea():
    
    s = []
    
    for ty in range(N):
        for y in range(1, S-1):
            sl = ""
            for tx in range(N):
                
                # top row
                if ty == 0:
                    if tx == 0: t = FIXED_CORNER_TILES[TileCorner.TopLeft]  # top-left
                    elif tx == N - 1: t = FIXED_CORNER_TILES[TileCorner.TopRight]  # top-right
                    else: t = FIXED_SIDE_TILES[TileSide.Top][tx - 1]  # top side

                # bottom row
                elif ty == N - 1:
                    if tx == N - 1: t = FIXED_CORNER_TILES[TileCorner.BottomRight]  # bottom-right
                    elif tx == 0: t = FIXED_CORNER_TILES[TileCorner.BottomLeft]  # bottom-left
                    else: t = FIXED_SIDE_TILES[TileSide.Bottom][N - (tx + 2)]  # bottom side

                # middle rows
                else:
                    if tx == N - 1: t = FIXED_SIDE_TILES[TileSide.Right][ty - 1]  # right side
                    elif tx == 0: t = FIXED_SIDE_TILES[TileSide.Left][N - (ty + 2)]  # left side
                    else: t = FIXED_CENTER_TILES[ty-1][tx-1]

                sl += t.ch_mid(y)
                
            s.append(sl)

    return s


def fill_sea_monster(s, x0, y0):
    for y in range(len(MONSTER)):
        monster_row = MONSTER[y]
        sea_row = s[y0+y]
        sea_row_new = ""
        for x in range(len(sea_row)):
            sea_ch = sea_row[x]
            if x0 <= x <= (x0 + (len(monster_row)-1)):
                if monster_row[x-x0] == '#':
                    sea_ch = 'O'
            sea_row_new += sea_ch
        s[y0+y] = sea_row_new


def find_monsters(s):
    sea_side = N * (S-2)

    num = 0
    for y in range(sea_side - (len(MONSTER)-1)):
        for x in range(sea_side - (len(MONSTER[0])-1)):
            if find_monster_worker(s, x, y):
                fill_sea_monster(s, x, y)
                num += 1

    return num


def find_monster_worker(sea, x0, y0):

    for y in range(len(MONSTER)):
        monster_row = MONSTER[y]
        for x in range(len(monster_row)):
            if monster_row[x] == '#' and sea[y0+y][x0+x] == '.': return False

    return True


def sea_rotate(sea):
    zea = []
    for y in range(len(sea)):
        zea_row = ""
        for x in range(len(sea)):
            zea_row += sea[-(x+1)][y]
        zea.append(zea_row)

    for y in range(len(sea)):
        sea[y] = zea[y]


def sea_mirror(sea):
    for y in range(len(sea)):
        sea[y] = sea[y][::-1]

def calc_roughness(sea):
    r = 0
    for y in range(len(sea)):
        for x in range(len(sea)):
            if sea[y][x] == '#': r += 1
    return r


def main():
    load_tiles()
    scan_edge_marks()
    find_corner_and_side_tiles()
    dump_corner_ids()
    start_assembly()
    assemble_frame()
#   dump_entire_table()
    assemble_center()
#   dump_entire_table()
    sea = compress_sea()
#   dump_sea(sea)

    for i in range(2):
        for j in range(4):
            n = find_monsters(sea)
            if n > 0:
                r = calc_roughness(sea)
                dump_sea(sea)
                print("r: %d" % r)
                return
            sea_rotate(sea)
        sea_mirror(sea)
    raise RuntimeError


if __name__ == '__main__':
    main()
