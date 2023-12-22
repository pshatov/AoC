import sys
import numpy as np

from copy import deepcopy
from enum import Enum, auto
from dataclasses import dataclass, replace
from typing import Tuple, List, Dict, Optional


class Dir(Enum):
    Up = auto()
    Down = auto()
    Left = auto()
    Right = auto()


@dataclass
class XY:
    x: int
    y: int

    def __eq__(self, other: 'XY') -> bool:
        return self.x == other.x and self.y == other.y


#  |  |    |
#  |  L-  -J  -7  F-  ---
#  |           |  |


def calc_num_walls(walls: str) -> int:
    num_walls = 0
    walls = walls.replace('-', '')
    while len(walls) > 0:
        if walls.startswith('|'):
            num_walls += 1
            walls = walls[1:]
        elif walls.startswith("F7"):
            walls = walls[2:]
        elif walls.startswith("FJ"):
            num_walls += 1
            walls = walls[2:]
        elif walls.startswith("L7"):
            num_walls += 1
            walls = walls[2:]
        elif walls.startswith("LJ"):
            walls = walls[2:]
        else:
            raise RuntimeError
        
    return num_walls


def load_input(filename: str) -> Tuple[XY, List[str]]:

    with open(filename) as f:
        all_lines = [l for l in [l.strip() for l in f] if l]

    xy0 = None
    for y0, next_line in enumerate(all_lines):
        if 'S' in next_line:
            x0 = next_line.find('S')
            xy0 = XY(x0, y0)
            break
        
    assert xy0 is not None

    return xy0, all_lines


def store_initial_dir(dir1: Dir, dir2: Dir, d: Dir) -> Tuple[Dir, Dir]:
    if dir1 is None:
        dir1 = d
    else:
        if dir2 is None:
            dir2 = d
        else:
            raise RuntimeError
    return dir1, dir2


def get_next_tile(all_lines: List[str], xy: XY, dir: Dir) -> str:
    if dir == Dir.Up:
        return all_lines[xy.y - 1][xy.x]
    elif dir == Dir.Down:
        return all_lines[xy.y + 1][xy.x]
    elif dir == Dir.Left:
        return all_lines[xy.y][xy.x - 1]
    elif dir == Dir.Right:
        return all_lines[xy.y][xy.x + 1]
    else:
        raise RuntimeError
    

def advance_xy(xy: XY, dir: Dir) -> XY:
    if dir == Dir.Up:
        xy.y -= 1
    elif dir == Dir.Down:
        xy.y += 1
    elif dir == Dir.Left:
        xy.x -= 1
    elif dir == Dir.Right:
        xy.x += 1
    else:
        raise RuntimeError

    return xy


def update_next_dir(all_lines: List[str], xy: XY, dir: Dir) -> Dir:

    tile = all_lines[xy.y][xy.x]

    if dir == Dir.Up:
        if tile == "|":
            return Dir.Up
        if tile == "7":
            return Dir.Left
        if tile == "F":
            return Dir.Right
        
    if dir == Dir.Down:
        if tile == "|":
            return Dir.Down
        if tile == "L":
            return Dir.Right
        if tile == "J":
            return Dir.Left

    if dir == Dir.Left:
        if tile == "-":
            return Dir.Left
        if tile == "L":
            return Dir.Up
        if tile == "F":
            return Dir.Down

    if dir == Dir.Right:
        if tile == "-":
            return Dir.Right
        if tile == "J":
            return Dir.Up
        if tile == "7":
            return Dir.Down

    raise RuntimeError


def part1(filename: str) -> Tuple[List[List[str]], int]:
    xy0, all_lines = load_input(filename)

    field = []

    dir1, dir2 = None, None
    for d in Dir:
        if d == Dir.Up:
            next_tile = get_next_tile(all_lines, xy0, d)
            if next_tile in "|7F":
                dir1, dir2 = store_initial_dir(dir1, dir2, d)
        elif d == Dir.Down:
            next_tile = get_next_tile(all_lines, xy0, d)
            if next_tile in "|LJ":
                dir1, dir2 = store_initial_dir(dir1, dir2, d)                
        elif d == Dir.Left:
            next_tile = get_next_tile(all_lines, xy0, d)
            if next_tile in "-LF":
                dir1, dir2 = store_initial_dir(dir1, dir2, d)
        elif d == Dir.Right:
            next_tile = get_next_tile(all_lines, xy0, d)
            if next_tile in "-J7":
                dir1, dir2 = store_initial_dir(dir1, dir2, d)

    xy1 = replace(xy0)
    xy2 = replace(xy0)
    steps = 0

    for y in range(len(all_lines)):
        field.append([])
        for x in range(len(all_lines[y])):
            field[y].append(".")

    if dir1 == Dir.Up:
        if dir2 == Dir.Down:
            field[xy0.y][xy0.x] = "|"
        else:
            raise RuntimeError
    else:
        raise RuntimeError

    while steps == 0 or xy1 != xy2:
        
        xy1 = advance_xy(xy1, dir1)
        xy2 = advance_xy(xy2, dir2)

        field[xy1.y][xy1.x] = all_lines[xy1.y][xy1.x]
        field[xy2.y][xy2.x] = all_lines[xy2.y][xy2.x]

        dir1 = update_next_dir(all_lines, xy1, dir1)
        dir2 = update_next_dir(all_lines, xy2, dir2)

        steps += 1

    return field, steps


def part2(field: List[List[str]]) -> int:

    for y in range(len(field)):
        assert field[y][0] == '.'

    field_new = deepcopy(field)

    total = 0
    for y in range(len(field)):
        for x_point in range(1, len(field[y])):
            if field[y][x_point] != '.':
                continue
            walls = ""
            for x in range(x_point):
                if field[y][x] != '.':
                    walls += field[y][x]
            num_walls = calc_num_walls(walls)
            if num_walls % 2 > 0:
                field_new[y][x_point] = "X"
                total += 1

    for y in range(len(field)):
        for x in range(len(field[y])):
            print(field[y][x], end='')
        print()

    print("---")

    for y in range(len(field_new)):
        for x in range(len(field_new[y])):
            print(field_new[y][x], end='')
        print()

    return total


def main() -> int:

    field, answer1 = part1('day_10_input.txt')
    answer2 = part2(field)

    print(f"{answer1}")
    print(f"{answer2}")

    return 0


if __name__ == '__main__':
    sys.exit(main())
