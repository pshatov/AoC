import sys
import numpy as np

from enum import Enum, auto
from functools import reduce
from numpy import ndarray
from typing import Tuple, List, Dict, Optional


class Dir(Enum):
    North = auto()
    West = auto()
    South = auto()
    East = auto()


def load_input(filename: str) -> ndarray:

    with open(filename) as f:
        all_lines = [l.strip() for l in f]

    while all_lines[-1] == "":
        del all_lines[-1]

    dy = len(all_lines)
    dx = len(all_lines[0])

    platform = np.zeros((dy, dx), dtype=np.int_)
    for y in range(dy):
        for x in range(dx):
            if all_lines[y][x] == '#':
                platform[y, x] = 1
            elif all_lines[y][x] == 'O':
                platform[y, x] = 2

    return platform


def move(platform: ndarray, dir: Dir) -> None:

    replace_lut = {Dir.North: ('02', '20'),
                   Dir.South: ('20', '02'),
                   Dir.West: ('02', '20'),
                   Dir.East: ('20', '02'),
                   }

    dy, dx = platform.shape

    if dir == Dir.North or dir == Dir.South:
        vs_old, vs_new = replace_lut[dir]
        for x in range(dx):
            v = platform[:, x]
            vs = ''.join([str(t) for t in v])
            while vs_old in vs:
                vs = vs.replace(vs_old, vs_new)
            for y in range(dy):
                platform[y, x] = int(vs[y])

    if dir == Dir.West or dir == Dir.East:
        hs_old, hs_new = replace_lut[dir]
        for y in range(dy):
            h = platform[y, :]
            hs = ''.join([str(t) for t in h])
            while hs_old in hs:
                hs = hs.replace(hs_old, hs_new)
            for x in range(dx):
                platform[y, x] = int(hs[x])


def calc_load(platform: ndarray, dir: Dir = Dir.North) -> int:

    assert dir == Dir.North

    dy, dx = platform.shape

    total = 0
    for y in range(dy):
        for x in range(dx):
            if platform[y, x] == 2:
                total += dy - y

    return total


def part1(filename: str) -> Tuple[ndarray, int]:
    
    platform = load_input(filename)
    platform_north = platform.copy()

    move(platform_north, Dir.North)
    
    total = calc_load(platform_north)

    return platform, total


def part2(platform: ndarray, num_iters: int = 1000000000) -> int:

    previous_loads = [calc_load(platform)]
    previous_platforms = [platform.copy()]

    keep_moving = True
    while keep_moving:
        move(platform, Dir.North)
        move(platform, Dir.West)
        move(platform, Dir.South)
        move(platform, Dir.East)

        if False:
            dy, dx = platform.shape
            print_lut = {0: '.',
                        1: '#',
                        2: 'O'}
            for y in range(dy):
                for x in range(dx):
                    print(f"{print_lut[platform[y, x]]}", end='')
                print()

        load = calc_load(platform)

        if load not in previous_loads:
            previous_loads.append(load)
            previous_platforms.append(platform.copy())
        else:
            possible_j = [i for i in range(len(previous_loads)) if previous_loads[i] == load]
            for j in possible_j:
                if np.array_equal(platform, previous_platforms[j]):
                    n0 = j
                    n1 = len(previous_platforms) - n0
                    k = (num_iters - n0) // n1
                    index = num_iters - k * n1
                    z = previous_loads[index]
                    print("!!!")
                    break
            else:
                previous_loads.append(load)
                previous_platforms.append(platform.copy())


    # total_horizontal = 0

    # for next_field in fields:
        
    #     vertical_counts = {}
    #     for next_row in next_field.axes_vertical_by_row:
    #         for x in next_row:
    #             if x not in vertical_counts:
    #                 vertical_counts[x] = 0
    #             vertical_counts[x] += 1

    #     horizontal_counts = {}
    #     for next_column in next_field.axes_horizontal_by_column:
    #         for y in next_column:
    #             if y not in horizontal_counts:
    #                 horizontal_counts[y] = 0
    #             horizontal_counts[y] += 1

    #     v = [x for x in vertical_counts if vertical_counts[x] == next_field.dy - 1]            
    #     h = [y for y in horizontal_counts if horizontal_counts[y] == next_field.dx - 1]

    #     assert len(h) + len(v) == 1

    #     total_vertical += sum(v)
    #     total_horizontal += sum(h)

    # total = total_vertical + 100 * total_horizontal

    total = 0

    return total


def main() -> int:

    platform, answer1 = part1('day_14_input.txt')
    print(f"{answer1}")

    answer2 = part2(platform)
    print(f"{answer2}")

    return 0


if __name__ == '__main__':
    sys.exit(main())
