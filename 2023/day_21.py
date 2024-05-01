import sys
import networkx as nx
import numpy as np

from enum import Enum
from dataclasses import dataclass
from networkx import DiGraph
from typing import Tuple, Dict, List


@dataclass
class XY:
    x: int
    y: int


def load_input(filename: str) -> Tuple[np.ndarray, XY]:

    with open(filename) as f:
        all_lines = [l for l in [l.strip() for l in f] if l]

    dy = len(all_lines)
    dx = len(all_lines[0])
    shape = dy, dx

    field = np.zeros(shape, dtype=np.int_)

    xy = XY(-1, -1)
    for y in range(dy):
        for x in range(dx):
            if all_lines[y][x] == '.':
                pass
            elif all_lines[y][x] == '#':
                field[y, x] = -1
            elif all_lines[y][x] == 'S':
                xy.y = y
                xy.x = x
            else:
                raise RuntimeError
            
    assert xy.x >= 0 and xy.y >= 0

    return field, xy


def propagate(field: np.ndarray, step: int) -> None:
    dy, dx = field.shape

    for y in range(dy):
        for x in range(dx):
            
            if field[y, x] != step:
                continue

            if x > 0 and field[y, x - 1] >= 0:
                field[y, x - 1] = step + 1
            if x < dx - 1 and field[y, x + 1] >= 0:
                field[y, x + 1] = step + 1

            if y > 0 and field[y - 1, x] >= 0:
                field[y - 1, x] = step + 1
            if y < dy - 1 and field[y + 1, x] >= 0:
                field[y + 1, x] = step + 1


def part1(filename: str) -> Tuple[DiGraph, int]:
    
    field, xy = load_input(filename)

    n0 = 64

    field[xy.y, xy.x] = 1
    for n in range(1, n0 + 1):
        propagate(field, n)

    total = 0
    dy, dx = field.shape
    for y in range(dy):
        for x in range(dx):
            if field[y, x] == -1:
                s = '#'
            elif field[y, x] == n0 + 1:
                total += 1
                s = 'O'
            else:
                s = '.'
            print(s, end='')

        print()

    return field, xy, total


# def part2(steps: List[str]) -> int:

#     lens_by_box: List[List[Lens]] = []
#     for i in range(256):
#         lens_by_box.append([])

#     for next_step in steps:
#         label = ""
#         for i in range(len(next_step)):
#             if not next_step[i].isalpha():
#                 break
#         label = next_step[:i]
#         box_index = aoc_hash(label)
#         op = next_step[i]
#         box = lens_by_box[box_index]
#         if op == '-':
#             remove_index = -1
#             for i, lens in enumerate(box):
#                 if lens.label == label:
#                     remove_index = i
#                     break
#             if remove_index != -1:
#                 del box[remove_index]
#         elif op == '=':
#             power = int(next_step[i + 1:])
#             replace_index = -1
#             for i, lens in enumerate(box):
#                 if lens.label == label:
#                     replace_index = i
#                     break
#             if replace_index != -1:
#                 box[replace_index] = Lens(label, power)
#             else:
#                 box.append(Lens(label, power))
#         else:
#             raise RuntimeError

#         if False:
#             print(f'After "{next_step}":')
#             for i, box in enumerate(lens_by_box):
#                 if len(box) > 0:
#                     print(f'Box {i}:', end='')
#                     for lens in box:
#                         print(f' [{lens.label} {lens.power}]', end='')
#                     print('\n')

#     total = 0
#     for i, box in enumerate(lens_by_box):
#         for j, lens in enumerate(box):
#             power = (i + 1) * (j + 1) * lens.power
#             total += power

#     return total


def main() -> int:

    field, xy, answer1 = part1('day_21_input.txt')
    print(f"{answer1}")

    # answer2 = part2(steps)
    # print(f"{answer2}")

    return 0


if __name__ == '__main__':
    sys.exit(main())
