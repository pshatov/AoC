# ---------------------------------------------------------------------------------------------------------------------
# 14.py
# ---------------------------------------------------------------------------------------------------------------------
# AoC '22
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
# TODO: Very slow!
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------------------------------------------------
import numpy as np


# ---------------------------------------------------------------------------------------------------------------------
# More Imports
# ---------------------------------------------------------------------------------------------------------------------
from enum import Enum
from typing import Tuple, List, Optional


# ---------------------------------------------------------------------------------------------------------------------
class Tile(int, Enum):
    Air = 0
    Rock = 1
    Sand = 2
    Fixed = 3
    Bottom = 4
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
class XY:

    # -----------------------------------------------------------------------------------------------------------------
    def __init__(self, xy: str) -> None:
        xy_parts = xy.split(',')
        assert len(xy_parts) == 2
        self.x, self.y = [int(t) for t in xy_parts]
    # -----------------------------------------------------------------------------------------------------------------

    # -----------------------------------------------------------------------------------------------------------------
    def __repr__(self) -> str:
        return "<%d,%d>" % (self.x, self.y)
    # -----------------------------------------------------------------------------------------------------------------

    # -----------------------------------------------------------------------------------------------------------------
    @staticmethod
    def from_xy(xy: 'XY') -> 'XY':
        return XY("%s,%s" % (xy.x, xy.y))
    # -----------------------------------------------------------------------------------------------------------------

    # -----------------------------------------------------------------------------------------------------------------
    @staticmethod
    def from_x_y(x: int, y: int) -> 'XY':
        return XY("%s,%s" % (x, y))
    # -----------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
class Cave:

    # -----------------------------------------------------------------------------------------------------------------
    def __init__(self, dx: int, dy: int, min_x) -> None:
        self._offset_x = min_x - 1
        cave_shape = dy, dx
        self._cave = np.zeros(cave_shape, dtype=np.int_)
    # -----------------------------------------------------------------------------------------------------------------

    # -----------------------------------------------------------------------------------------------------------------
    def _cave_x(self, xy: XY) -> int:
        return xy.x - self._offset_x
    # -----------------------------------------------------------------------------------------------------------------

    # -----------------------------------------------------------------------------------------------------------------
    def mark_tile(self, xy: XY, tile: Tile) -> None:
        # FIXME: place 'self._cave_x(xy)' into [xy.y, x]!
        x = self._cave_x(xy)
        self._cave[xy.y, x] = tile
    # -----------------------------------------------------------------------------------------------------------------

    # -----------------------------------------------------------------------------------------------------------------
    def clear_tile(self, xy: XY) -> None:
        self._cave[xy.y, self._cave_x(xy)] = Tile.Air
    # -----------------------------------------------------------------------------------------------------------------

    # -----------------------------------------------------------------------------------------------------------------
    def get_tile(self, xy: XY) -> Tile:
        return self._cave[xy.y, self._cave_x(xy)]
    # -----------------------------------------------------------------------------------------------------------------

    # -----------------------------------------------------------------------------------------------------------------
    def advance_sand(self, xy: XY) -> Optional[XY]:
        x, y = self._cave_x(xy), xy.y
        assert self._cave[y, x] == Tile.Sand

        rows, cols = self._cave.shape
        if x == cols - 1:
            self._cave = np.c_[self._cave, np.zeros(rows, dtype=np.int_)]
        elif x == 0:
            self._cave = np.c_[np.zeros(rows, dtype=np.int_), self._cave]
            self._offset_x -= 1
            x = self._cave_x(xy)

        if self._cave[y + 1, x] == Tile.Air:
            self._cave[y, x] = Tile.Air
            self._cave[y + 1, x] = Tile.Sand
            return XY.from_x_y(x + self._offset_x, y + 1)
        elif self._cave[y + 1, x - 1] == Tile.Air:
            self._cave[y, x] = Tile.Air
            self._cave[y + 1, x - 1] = Tile.Sand
            return XY.from_x_y(x + self._offset_x - 1, y + 1)
        elif self._cave[y + 1, x + 1] == Tile.Air:
            self._cave[y, x] = Tile.Air
            self._cave[y + 1, x + 1] = Tile.Sand
            return XY.from_x_y(x + self._offset_x + 1, y + 1)
        else:
            self._cave[y, x] = Tile.Fixed
            return None
    # -----------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def get_all_rocks(all_lines: List[str]) -> List[List[XY]]:
    all_rocks = []
    for next_line in all_lines:
        all_rocks.append([])
        line_parts = next_line.split(' -> ')
        assert len(line_parts) > 1
        for next_part in line_parts:
            all_rocks[-1].append(XY(next_part))
    return all_rocks
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def calc_min_max_xy(all_rocks: List[List[XY]]) -> Tuple[XY, XY]:

    min_xy, max_xy = None, None
    for next_rock in all_rocks:
        for next_node in next_rock:
            if min_xy is None:
                min_xy = XY.from_xy(next_node)
            else:
                if next_node.x < min_xy.x:
                    min_xy.x = next_node.x
                if next_node.y < min_xy.y:
                    min_xy.y = next_node.y

            if max_xy is None:
                max_xy = XY.from_xy(next_node)
            else:
                if next_node.x > max_xy.x:
                    max_xy.x = next_node.x
                if next_node.y > max_xy.y:
                    max_xy.y = next_node.y

    return min_xy, max_xy
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def rocks2cave(cave: Cave, all_rocks: List[List[XY]]) -> None:

    prev_node: Optional[XY]
    for next_rock in all_rocks:
        prev_node = None
        for next_node in next_rock:
            if prev_node is not None:
                if next_node.x == prev_node.x:
                    src_y = min(next_node.y, prev_node.y)
                    dst_y = max(next_node.y, prev_node.y)
                    for y in range(src_y, dst_y + 1):
                        cave.mark_tile(XY.from_x_y(next_node.x, y), Tile.Rock)
                elif next_node.y == prev_node.y:
                    src_x = min(next_node.x, prev_node.x)
                    dst_x = max(next_node.x, prev_node.x)
                    for x in range(src_x, dst_x + 1):
                        cave.mark_tile(XY.from_x_y(x, next_node.y), Tile.Rock)
                else:
                    raise RuntimeError
            prev_node = next_node
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def main() -> None:

    with open('input.txt') as file:
        all_lines = [line for line in [line.strip() for line in file] if line]

    all_rocks = get_all_rocks(all_lines)
    min_xy, max_xy = calc_min_max_xy(all_rocks)

    assert max_xy.y > 0
    min_xy.y = 0

    dx = max_xy.x - min_xy.x + 1 + 2
    dy = max_xy.y - min_xy.y + 1 + 1
    y_bottom = dy - 1
    cave = Cave(dx, dy, min_xy.x)
    rocks2cave(cave, all_rocks)

    x0, y0 = 500, 0
    num_units = 0
    keep_adding = True
    while keep_adding:

        xy = XY.from_x_y(x0, y0)
        cave.mark_tile(xy, Tile.Sand)

        keep_falling = True
        while keep_falling:
            xy = cave.advance_sand(xy)

            if xy is None:
                num_units += 1
                keep_falling = False
            elif xy.y == y_bottom:
                num_units += 1
                cave.mark_tile(xy, Tile.Fixed)
                keep_adding = False
                break

    print("part 1: %d" % num_units)

    keep_adding = True
    while keep_adding:

        xy = XY.from_x_y(x0, y0)
        t = cave.get_tile(xy)
        if t != Tile.Air:
            break
        cave.mark_tile(xy, Tile.Sand)

        keep_falling = True
        while keep_falling:
            xy = cave.advance_sand(xy)

            if xy is None:
                num_units += 1
                keep_falling = False
            elif xy.y == y_bottom:
                num_units += 1
                cave.mark_tile(xy, Tile.Fixed)
                keep_falling = False

    print("part 2: %d" % num_units)
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    main()
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
# End of File
# ---------------------------------------------------------------------------------------------------------------------
