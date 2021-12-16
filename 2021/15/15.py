# ---------------------------------------------------------------------------------------------------------------------
# AoC 2021
# ---------------------------------------------------------------------------------------------------------------------
# 15.py
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------------------------------------------------
import sys


# ---------------------------------------------------------------------------------------------------------------------
# More Imports
# ---------------------------------------------------------------------------------------------------------------------
from copy import deepcopy
from enum import Enum, auto
from typing import List, Set, Tuple, Optional, Dict


# ---------------------------------------------------------------------------------------------------------------------
# Types
# ---------------------------------------------------------------------------------------------------------------------
MatrixInt = List[List[int]]
TupleXY = Tuple[int, int]
SetTupleXY = Set[TupleXY]
ListTupleXY = List[TupleXY]


# ---------------------------------------------------------------------------------------------------------------------
# Settings
# ---------------------------------------------------------------------------------------------------------------------
N = 5
XY1 = 100
XY2 = N * XY1

VT100_CLR_GRAY = "\033[38;2;80;80;80m"
VT100_CLR_RED = "\033[38;2;255;0;0m"


# ---------------------------------------------------------------------------------------------------------------------
class DijkstraClass:

    # -----------------------------------------------------------------------------------------------------------------
    class _NodeStateEnum(Enum):
        Unknown = auto()
        Computed = auto()
        Fixed = auto()
    # -----------------------------------------------------------------------------------------------------------------

    MatrixNodeStateEnum = List[List[_NodeStateEnum]]

    _node_risks: MatrixInt
    _node_weights: MatrixInt
    _node_states: MatrixNodeStateEnum
    _node_ancestors_dict: Dict[TupleXY, Optional[TupleXY]]

    _computed_node_weights_dict: Dict[int, List[TupleXY]]

    # -----------------------------------------------------------------------------------------------------------------
    def __init__(self, xy: int, risks: MatrixInt) -> None:

        self._node_risks = risks
        self._node_weights = list()
        self._node_states = list()
        self._node_ancestors_dict = dict()

        self._computed_node_weights_dict = dict()
        self._min_computed_node_weight = None

        self._xy = xy
        self._xy1 = xy - 1
        self._xy2 = self._xy * self._xy
        self._weight_inf = self._xy2 * 10

        for y in range(self._xy):
            self._node_weights.append([self._weight_inf] * self._xy)
            self._node_states.append([])
            for x in range(self._xy):
                # self._node_ancestors_dict[x, y] = None
                self._node_states[-1].append(self._NodeStateEnum.Unknown)
    # -----------------------------------------------------------------------------------------------------------------

    # -----------------------------------------------------------------------------------------------------------------
    def start(self, x: int, y: int, weight: int) -> None:

        self._node_weights[y][x] = weight
        self._node_states[y][x] = self._NodeStateEnum.Computed

        xy = x, y
        self._min_computed_node_weight = 0
        self._computed_node_weights_dict[self._min_computed_node_weight] = [xy]
    # -----------------------------------------------------------------------------------------------------------------

    # -----------------------------------------------------------------------------------------------------------------
    def _get_closest_computed_node(self) -> TupleXY:
        return self._computed_node_weights_dict[self._min_computed_node_weight][0]
    # -----------------------------------------------------------------------------------------------------------------

    # -----------------------------------------------------------------------------------------------------------------
    def step(self) -> bool:

        # get the closest computed node and its weight
        cc_xy = self._get_closest_computed_node()
        cc_x, cc_y = cc_xy

        # get adjacent not yet fixed nodes
        not_fixed_xy = self._get_not_fixed_nodes(cc_xy)
        for x, y in not_fixed_xy:

            # get next adjacent node weight
            weight = self._node_weights[cc_y][cc_x] + self._node_risks[y][x]

            # for not yet visited nodes just store the computed weight
            if self._node_states[y][x] == self._NodeStateEnum.Unknown:

                # update weight dict
                self._store_weight(weight, (x, y))

                # store weight, mark node as computed
                self._node_states[y][x] = self._NodeStateEnum.Computed

                # store ancestor node for later path reconstruction
                self._node_ancestors_dict[x, y] = cc_xy

            # for already visited nodes check, whether a smaller weight was found
            elif self._node_states[y][x] == self._NodeStateEnum.Computed:

                if weight < self._node_weights[y][x]:

                    # update weight dict
                    self._replace_weight(weight, (x, y))

                    # store ancestor node for later path reconstruction
                    self._node_ancestors_dict[x, y] = cc_xy

        # check, that the very last node was reached
        if cc_xy == (self._xy1, self._xy1):
            return True

        # update weight dict
        self._delete_weight(cc_xy)

        # fix the closest computed node
        self._node_states[cc_y][cc_x] = self._NodeStateEnum.Fixed

        return False
    # -----------------------------------------------------------------------------------------------------------------

    # -----------------------------------------------------------------------------------------------------------------
    def _get_not_fixed_nodes(self, computed_xy: TupleXY) -> SetTupleXY:

        x0, y0 = computed_xy
        xyl, xyr = (x0 - 1, y0), (x0 + 1, y0)
        xyt, xyb = (x0, y0 - 1), (x0, y0 + 1)

        potential_xy = set()

        if y0 > 0:
            potential_xy.add(xyt)
        if x0 > 0:
            potential_xy.add(xyl)
        if y0 < (self._xy - 1):
            potential_xy.add(xyb)
        if x0 < (self._xy - 1):
            potential_xy.add(xyr)

        fixed_xy = set()
        for x, y in potential_xy:
            if self._node_states[y][x] == self._NodeStateEnum.Fixed:
                fixed_xy.add((x, y))

        return potential_xy - fixed_xy
    # -----------------------------------------------------------------------------------------------------------------

    # -----------------------------------------------------------------------------------------------------------------
    def weight(self, x: int, y: int) -> int:
        return self._node_weights[y][x]
    # -----------------------------------------------------------------------------------------------------------------

    # -----------------------------------------------------------------------------------------------------------------
    def _store_weight(self, weight: int, xy: TupleXY) -> None:

        x, y = xy

        # update matrix
        self._node_weights[y][x] = weight

        # add key if necessary
        if weight not in self._computed_node_weights_dict.keys():
            self._computed_node_weights_dict[weight] = []

        # store weight
        self._computed_node_weights_dict[weight].append(xy)

        # update cache
        if weight < self._min_computed_node_weight:
            self._min_computed_node_weight = weight
    # -----------------------------------------------------------------------------------------------------------------

    # -----------------------------------------------------------------------------------------------------------------
    def _replace_weight(self, new_weight: int, xy: TupleXY) -> None:
        self._delete_weight(xy)
        self._store_weight(new_weight, xy)
    # -----------------------------------------------------------------------------------------------------------------

    # -----------------------------------------------------------------------------------------------------------------
    def _delete_weight(self, xy: TupleXY) -> None:

        x, y = xy
        w = self._node_weights[y][x]

        # delete
        self._computed_node_weights_dict[w].remove(xy)

        # update cache if necessary
        if len(self._computed_node_weights_dict[w]) == 0:
            del self._computed_node_weights_dict[w]
            self._min_computed_node_weight = min(self._computed_node_weights_dict.keys())
    # -----------------------------------------------------------------------------------------------------------------

    # -----------------------------------------------------------------------------------------------------------------
    def path(self) -> List[TupleXY]:

        path_list = [(self._xy1, self._xy1)]

        follow = True
        while follow:
            prev_xy = self._node_ancestors_dict[path_list[-1]]
            path_list.append(prev_xy)
            if prev_xy == (0, 0):
                follow = False

        return path_list
    # -----------------------------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def extend_cavern(cavern1: MatrixInt) -> MatrixInt:

    cavern2 = deepcopy(cavern1)

    for y in range(XY1):
        for nx in range(1, N):
            for x in range(XY1):
                v_new = (cavern2[y][XY1 * (nx - 1) + x] + 1)
                v_new = 1 if v_new > 9 else v_new
                cavern2[y].append(v_new)
                continue

    for ny in range(1, N):
        for y in range(XY1):
            cavern2.append([])
            for x in range(XY1 * N):
                v_new = (cavern2[XY1 * (ny - 1) + y][x] + 1)
                v_new = 1 if v_new > 9 else v_new
                cavern2[XY1 * ny + y].append(v_new)

    return cavern2
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def draw_cavern(cavern: MatrixInt, path: ListTupleXY) -> None:
    for y in range(len(cavern)):
        for x in range(len(cavern[y])):
            xy = x, y
            if xy in path:
                sys.stdout.write(VT100_CLR_RED)
            print("%d" % cavern[y][x], end='')
            if xy in path:
                sys.stdout.write(VT100_CLR_GRAY)
        print()
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def main() -> None:

    with open('input.txt') as f:
        f_lines = [t.strip() for t in f.readlines()]

    cavern1: MatrixInt
    cavern2: MatrixInt

    cavern1 = []
    for y in range(XY1):
        cavern1.append([int(t) for t in f_lines[y]])

    cavern2 = extend_cavern(cavern1)

    dijkstra1 = DijkstraClass(XY1, cavern1)
    dijkstra1.start(0, 0, 0)

    finished = False
    while not finished:
        finished = dijkstra1.step()

    w = dijkstra1.weight(XY1 - 1, XY1 - 1)
    assert sum([cavern1[ty][tx] for tx, ty in dijkstra1.path()]) == w + cavern1[0][0]
    print("part 1: %d" % w)

    draw_cavern(cavern1, dijkstra1.path())

    dijkstra2 = DijkstraClass(XY2, cavern2)
    dijkstra2.start(0, 0, 0)

    finished = False
    while not finished:
        finished = dijkstra2.step()

    w = dijkstra2.weight(XY2 - 1, XY2 - 1)
    assert sum([cavern2[ty][tx] for tx, ty in dijkstra2.path()]) == w + cavern2[0][0]
    print("part 2: %d" % w)

    # WARNING: Huge, re-enable at your own risk!
    if False:
        draw_cavern(cavern2, dijkstra2.path())
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    main()
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
# End of File
# ---------------------------------------------------------------------------------------------------------------------
