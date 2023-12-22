import sys

import numpy as np

from enum import Enum
from dataclasses import dataclass
from typing import Tuple, List, Dict, Optional


@dataclass
class XY:
    x: int
    y: int

    @property
    def xy(self) -> Tuple[int, int]:
        return self.x, self.y
    
    def __eq__(self, other: object) -> bool:
        return self.x == other.x and self.y == other.y


class Dir(Enum):
    Up = "U"
    Down = "D"
    Left = "L"
    Right = "R"


@dataclass
class Side:
    dir: Dir
    length: int
    color: int


def load_input(filename: str) -> List[Side]:

    with open(filename) as f:
        lines = [l for l in [l.strip() for l in f] if l]

    sides = []
    for next_line in lines:
        dir, length, color = next_line.split(' ')
        assert color.startswith('(#')
        assert color.endswith(')')
        sides.append(Side(Dir(dir), int(length), int(color[2:-1], 16)))

    return sides


def step(field: np.ndarray, xy: XY, dir: Dir, color: int) -> None:

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

    rows, cols = field.shape

    if xy.x < 0:
        assert xy.x == -1
        xy.x = 0
        shape = rows, 1
        h = np.zeros(shape, dtype=np.int_), field
        field = np.hstack(h)

    if xy.y < 0:
        assert xy.y == -1
        xy.y = 0
        shape = 1, cols
        v = np.zeros(shape, dtype=np.int_), field
        field = np.vstack(v)

    if xy.x > cols - 1:
        assert xy.x == cols
        shape = rows, 1
        h = field, np.zeros(shape, dtype=np.int_)
        field = np.hstack(h)

    if xy.y > rows - 1:
        assert xy.y == rows
        shape = 1, cols
        v = field, np.zeros(shape, dtype=np.int_)
        field = np.vstack(v)

    field[xy.y, xy.x] = color

    return field


def append_layer(layer: List[XY], xy: XY) -> None:
    for next_xy in layer:
        if next_xy == xy:
            return

    layer.append(xy)
        

def fill_field_iterative(field: np.ndarray, layer: List[XY]) -> None:

    rows, cols = field.shape

    next_layer = []
    for next_xy in layer:
        x, y = next_xy.xy
        
        assert field[y, x] == 0
        field[y, x] = -1

        if y > 0 and field[y - 1, x] == 0:
            append_layer(next_layer, XY(x, y - 1))

        if y < rows - 1 and field[y + 1, x] == 0:
            append_layer(next_layer, XY(x, y + 1))

        if x > 0 and field[y, x - 1] == 0:
            append_layer(next_layer, XY(x - 1, y))

        if x < cols - 1 and field[y, x + 1] == 0:
            append_layer(next_layer, XY(x + 1, y))

    return next_layer


def fill_field(field: np.ndarray) -> None:

    rows, cols = field.shape
    shape_h = rows, 1

    new_field = field
    h = np.zeros(shape_h, dtype=np.int_), new_field, np.zeros(shape_h, dtype=np.int_)
    new_field = np.hstack(h)

    shape_v = 1, cols + 2
    v = np.zeros(shape_v, dtype=np.int_), new_field, np.zeros(shape_v, dtype=np.int_)
    new_field = np.vstack(v)

    print("fill_field()")

    i = 0
    next_layer = [XY(0, 0)]
    while len(next_layer) > 0:
        l0 = len(next_layer)
        next_layer = fill_field_iterative(new_field, next_layer)
        i += 1
        print(f"iter {i}: {l0} -> {len(next_layer)}")

    for y in range(rows):
        for x in range(cols):
            field[y, x] = new_field[y + 1, x + 1]


def part1(filename: str) -> Tuple[List[Side], np.ndarray, int]:
    
    sides = load_input(filename)

    shape = 1, 1
    field = np.zeros(shape, dtype=np.int_)
    field[0, 0] = -1
    
    xy = XY(0, 0)
    for next_side in sides:
        for i in range(next_side.length):
            field = step(field, xy, next_side.dir, next_side.color)

    fill_field(field)

    total = 0
    dy, dx = field.shape
    for y in range(dy):
        for x in range(dx):
            if field[y, x] >= 0:
                total += 1

    return sides, field, total


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

    sides, field, answer1 = part1('day_18_input.txt')
    print(f"{answer1}")

    # answer2 = part2(steps)
    # print(f"{answer2}")

    return 0


if __name__ == '__main__':
    sys.exit(main())
