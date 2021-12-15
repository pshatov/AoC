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
from enum import Enum, auto
from typing import List, Set, Tuple, Optional, Dict
from copy import deepcopy


# ---------------------------------------------------------------------------------------------------------------------
# Types
# ---------------------------------------------------------------------------------------------------------------------
TupleXY = Tuple[int, int]
SetTupleXY = Set[TupleXY]


# ---------------------------------------------------------------------------------------------------------------------
# Settings
# ---------------------------------------------------------------------------------------------------------------------
XY = None
N = 4

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

    _node_risks: List[List[int]]
    _node_weights: List[List[int]]
    _node_states: List[List[_NodeStateEnum]]
    _node_prevs: Dict[TupleXY, Optional[TupleXY]]

    _computed_xy_new: Dict[int, List[TupleXY]]

    # -----------------------------------------------------------------------------------------------------------------
    def __init__(self, xy: int, risks: List[List[int]]) -> None:

        self._node_risks = risks
        self._node_weights = []
        self._node_states = []
        self._node_prevs = {}
        self._xy = xy

        self._xy2 = self._xy * self._xy
        self._weight_inf = self._xy2 * 10

        for y in range(self._xy):
            self._node_weights.append([self._weight_inf] * self._xy)
            self._node_states.append([])
            for x in range(self._xy):
                xy = x, y
                self._node_prevs[xy] = None
                self._node_states[-1].append(self._NodeStateEnum.Unknown)

        self._computed_xy_new = dict()
        self._min_computed_xy_key = None
    # -----------------------------------------------------------------------------------------------------------------

    # -----------------------------------------------------------------------------------------------------------------
    def compute_weight_manual(self, x: int, y: int, weight: int) -> None:
        self._node_weights[y][x] = weight
        self._node_states[y][x] = self._NodeStateEnum.Computed

        xy = x, y
        self._min_computed_xy_key = 0
        self._computed_xy_new[self._min_computed_xy_key] = []
        self._computed_xy_new[self._min_computed_xy_key].append(xy)
    # -----------------------------------------------------------------------------------------------------------------

    # -----------------------------------------------------------------------------------------------------------------
    def _cc_xy(self) -> Tuple[int, TupleXY]:
        xy = self._computed_xy_new[self._min_computed_xy_key][0]
        x, y = xy
        return self._node_weights[y][x], xy
    # -----------------------------------------------------------------------------------------------------------------

    # -----------------------------------------------------------------------------------------------------------------
    def step(self) -> bool:

        closest_computed_weight, closest_computed_xy = self._cc_xy()

        if closest_computed_xy == (self._xy - 1, self._xy - 1):
            return True

        not_fixed_xy = self._get_not_fixed_xy(closest_computed_xy)

        cc_x, cc_y = closest_computed_xy

        for xy in not_fixed_xy:
            x, y = xy
            weight = self._node_weights[cc_y][cc_x] + self._node_risks[y][x]

            if self._node_states[y][x] == self._NodeStateEnum.Unknown:
                self._node_weights[y][x] = weight
                self._node_states[y][x] = self._NodeStateEnum.Computed

                if weight not in self._computed_xy_new.keys():
                    self._computed_xy_new[weight] = []
                    if weight < self._min_computed_xy_key:
                        self._min_computed_xy_key = weight

                self._computed_xy_new[weight].append(xy)

                self._node_prevs[xy] = closest_computed_xy

            elif self._node_states[y][x] == self._NodeStateEnum.Computed:
                if weight < self._node_weights[y][x]:
                    self._node_weights[y][x] = weight
                    self._node_prevs[xy] = closest_computed_xy

        self._node_states[cc_y][cc_x] = self._NodeStateEnum.Fixed

        self._computed_xy_new[closest_computed_weight].remove(closest_computed_xy)
        if len(self._computed_xy_new[closest_computed_weight]) == 0:
            del self._computed_xy_new[closest_computed_weight]
            self._min_computed_xy_key = min(self._computed_xy_new.keys())


        return False
    # -----------------------------------------------------------------------------------------------------------------

    def _z(self):
        self._closest_computed_xy = -1, -1
        self._closest_computed_weight = None
        for xy in self._computed_xy_:
            x, y = xy
            if self._closest_computed_weight is None or self._node_weights[y][x] < self._closest_computed_weight:
                self._closest_computed_xy = xy
                self._closest_computed_weight = self._node_weights[y][x]


    # -----------------------------------------------------------------------------------------------------------------
    def _get_not_fixed_xy(self, computed_xy: TupleXY) -> SetTupleXY:

        x0, y0 = computed_xy
        xyl, xyr = (x0 - 1, y0), (x0 + 1, y0)
        xyt, xyb = (x0, y0 - 1), (x0, y0 + 1)

        all_xy = set()

        if y0 > 0:
            all_xy.add(xyt)
        if x0 > 0:
            all_xy.add(xyl)
        if y0 < (self._xy - 1):
            all_xy.add(xyb)
        if x0 < (self._xy - 1):
            all_xy.add(xyr)

        fixed_xy = set()
        for xy in all_xy:
            x, y = xy
            if self._node_states[y][x] == self._NodeStateEnum.Fixed:
                fixed_xy.add(xy)

        return all_xy - fixed_xy
    # -----------------------------------------------------------------------------------------------------------------

    # -----------------------------------------------------------------------------------------------------------------
    def weight(self, x: int, y: int) -> int:
        return self._node_weights[y][x]
    # -----------------------------------------------------------------------------------------------------------------

    # -----------------------------------------------------------------------------------------------------------------
    def path(self) -> List[TupleXY]:

        path_list = [(self._xy - 1, self._xy - 1)]

        follow = True
        while follow:
            prev_xy = self._node_prevs[path_list[-1]]
            path_list.append(prev_xy)
            if prev_xy == (0, 0):
                follow = False

        return path_list
    # -----------------------------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def main() -> None:

    global XY

    with open('input.txt') as f:
        f_lines = [t.strip() for t in f.readlines()]

    XY = len(f_lines)

    cavern = []
    for y in range(XY):
        cavern.append([int(t) for t in f_lines[y]])

    #dijkstra = DijkstraClass(XY, cavern)
    #dijkstra.compute_weight_manual(0, 0, 0)

    #finished = False
    #while not finished:
    #    finished = dijkstra.step()

    #print("part 1: %d" % dijkstra.weight(XY - 1, XY - 1))

    for y in range(XY):
        for x in range(N - 1):
            cavern[y].extend(deepcopy(cavern[y][0: XY]))

    for n in range(N - 1):
        for y in range(XY):
            cavern.append(deepcopy(cavern[y]))

    XY *= N

    dijkstra2 = DijkstraClass(XY, cavern)
    dijkstra2.compute_weight_manual(0, 0, 0)

    finished = False
    while not finished:
        finished = dijkstra2.step()

    print("!")

    # path = dijkstra.path()
    # for y in range(XY):
    #     for x in range(XY):
    #         xy = x, y
    #         if xy in path:
    #             sys.stdout.write(VT100_CLR_RED)
    #         print("%d" % cavern[y][x], end='')
    #         if xy in path:
    #             sys.stdout.write(VT100_CLR_GRAY)
    #     print()

# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    main()
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
# End of File
# ---------------------------------------------------------------------------------------------------------------------
