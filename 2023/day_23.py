import sys

from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class XY:
    x: int
    y: int


class Day23:

    _input_lines: List[str]
    _first_x: int
    _last_x: int
    _dy: int
    _dx: int

    def __init__(self, filename: str) -> None:

        sys.setrecursionlimit(10000)
        
        with open(filename) as f:
            self._input_lines = [l for l in [l.strip() for l in f] if l]
        
        self._dy = len(self._input_lines)
        self._dx = len(self._input_lines[0])

        self._first_x = self._input_lines[0].find('.')
        self._last_x = self._input_lines[-1].find('.')

    def _continue_routes_recursive(self, current_route: List[XY], routes: List[List[int]]) -> None:

        print(len(current_route))

        xy0 = current_route[-1]
        if xy0.y == self._dy - 1 and xy0.x == self._last_x:
            routes.append(current_route)
            return

        next_xy = []
        # up
        if xy0.y > 0 and self._input_lines[xy0.y - 1][xy0.x] != '#':
            next_xy.append(XY(xy0.x, xy0.y - 1))

        # down
        if xy0.y < self._dy - 1 and self._input_lines[xy0.y + 1][xy0.x] != '#':
            next_xy.append(XY(xy0.x, xy0.y + 1))

        # left
        if xy0.x > 0 and self._input_lines[xy0.y][xy0.x - 1] != '#':
            next_xy.append(XY(xy0.x - 1, xy0.y))

        # right
        if xy0.x < self._dx - 1 and self._input_lines[xy0.y][xy0.x + 1] != '#':
            next_xy.append(XY(xy0.x + 1, xy0.y))

        for xy in next_xy:

            if xy in current_route:
                continue

            if self._input_lines[xy.y][xy.x] == '.':
                self._continue_routes_recursive(current_route + [xy], routes)

            elif self._input_lines[xy.y][xy.x] == 'v':
                xy1 = XY(xy.x, xy.y + 1)
                if xy1 not in current_route:
                    assert self._input_lines[xy1.y][xy1.x] != '#'
                    self._continue_routes_recursive(current_route + [xy, xy1], routes)

            elif self._input_lines[xy.y][xy.x] == '>':
                xy1 = XY(xy.x + 1, xy.y)
                if xy1 not in current_route:
                    assert self._input_lines[xy1.y][xy1.x] != '#'
                    self._continue_routes_recursive(current_route + [xy, xy1], routes)

            else:
                raise RuntimeError

        

    def part1(self) -> int:

        routes = []
        self._continue_routes_recursive([XY(self._first_x, 0)], routes)
        length = max([len(r) for r in routes]) - 1
        return length
    
    def part2(self) -> int:
        return 0


t = Day23('data/day_23_input.txt')
print(t.part1())
