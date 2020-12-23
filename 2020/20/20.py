TILES = {}
EDGES = {}
CORNER_TILES = {}


class Tile:

    def __init__(self):
        self._T = []

    def store_row(self, r):
        self._T.append([])
        for i in range(len(r)):
            self._T[-1].append(r[i])

    @property
    def edge_top(self):
        e = ""
        for x in range(len(self._T[0])):
            e += self._T[0][x]
        return e

    @property
    def edge_bottom(self):
        e = ""
        for x in range(len(self._T[-1])):
            e += self._T[-1][x]
        return e

    @property
    def edge_left(self):
        e = ""
        for y in range(len(self._T)):
            e += self._T[y][0]
        return e

    @property
    def edge_right(self):
        e = ""
        for y in range(len(self._T)):
            e += self._T[y][-1]
        return e


def load_tiles():
    with open('input.txt') as f:
        f_lines = f.readlines()

    for li in range(0, len(f_lines), 12):
        ls = f_lines[li].strip()
        tile_id = int(ls.split(' ')[1][:-1])
        t = Tile()
        for j in range(1, 11):
            ls = f_lines[li+j].strip()
            t.store_row(ls)
        TILES[tile_id] = t


def scan_next_edge(edge):
    edge_rev = edge[::-1]
    if edge in EDGES.keys(): EDGES[edge] += 1
    elif edge_rev in EDGES.keys(): EDGES[edge_rev] += 1
    else: EDGES[edge] = 1


def scan_edges():

    for tile in TILES.values():

        edge_top = tile.edge_top
        edge_bottom = tile.edge_bottom
        edge_left = tile.edge_left
        edge_right = tile.edge_right

        scan_next_edge(edge_top)
        scan_next_edge(edge_bottom)
        scan_next_edge(edge_left)
        scan_next_edge(edge_right)

def find_next_corner_tile(edge):
    edge_rev = edge[::-1]
    if edge in EDGES and EDGES[edge] == 1: return True
    elif edge_rev in EDGES and EDGES[edge_rev] == 1: return True
    else: return False

def find_corner_tiles():

    for tile_id in TILES.keys():

        tile = TILES[tile_id]

        edge_top = tile.edge_top
        edge_bottom = tile.edge_bottom
        edge_left = tile.edge_left
        edge_right = tile.edge_right

        n = 0
        if find_next_corner_tile(edge_top): n += 1
        if find_next_corner_tile(edge_bottom): n += 1
        if find_next_corner_tile(edge_left): n += 1
        if find_next_corner_tile(edge_right): n += 1

        if n == 2:
            CORNER_TILES[tile_id] = tile

    for corner_tile_id in CORNER_TILES.keys():
        del TILES[corner_tile_id]


def main():
    load_tiles()
    scan_edges()
    find_corner_tiles()
    if len(CORNER_TILES) != 4: raise RuntimeError
    m = 1
    for z in CORNER_TILES.keys():
        m *= z
    print("m: %d" % m)




if __name__ == '__main__':
    main()