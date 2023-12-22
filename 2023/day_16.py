import sys

import numpy as np

from enum import Enum, auto
from dataclasses import dataclass
from typing import Tuple, List, Dict, Optional


class Dir(Enum):
    Up = auto()
    Down = auto()
    Left = auto()
    Right = auto()


@dataclass
class Beam:
    y: int
    x: int
    dir: Dir


class Field:
    dy: int
    dx: int
    lines: List[str]
    beams: List[Beam]
    mask: Optional[np.ndarray]

    def __init__(self, lines: List[str], beams: List[Beam]) -> None:
        self.lines = lines
        self.beams = beams
        self.dy = len(self.lines)
        self.dx = len(self.lines[0])
        self.mask = np.zeros((self.dy, self.dx), dtype=np.int_)

    def tick(self) -> None:

        beams = []
        for next_beam in self.beams:
            tile = self.lines[next_beam.y][next_beam.x]
            self.mask[next_beam.y, next_beam.x] = 1

            if tile == '.':
                if next_beam.dir == Dir.Right:
                    next_beam.x += 1
                elif next_beam.dir == Dir.Left:
                    next_beam.x -= 1
                elif next_beam.dir == Dir.Up:
                    next_beam.y -= 1
                elif next_beam.dir == Dir.Down:
                    next_beam.y += 1
                else:
                    raise RuntimeError
                beams.append(next_beam)

            elif tile == '|':
                if next_beam.dir == Dir.Right or next_beam.dir == Dir.Left:
                    beams.append(Beam(next_beam.y - 1, next_beam.x, Dir.Up))
                    beams.append(Beam(next_beam.y + 1, next_beam.x, Dir.Down))
                else:
                    if next_beam.dir == Dir.Up:
                        next_beam.y -= 1
                    elif next_beam.dir == Dir.Down:
                        next_beam.y += 1
                    else:
                        raise RuntimeError
                    beams.append(next_beam)

            elif tile == '-':
                if next_beam.dir == Dir.Down or next_beam.dir == Dir.Up:
                    beams.append(Beam(next_beam.y, next_beam.x - 1, Dir.Left))
                    beams.append(Beam(next_beam.y, next_beam.x + 1, Dir.Right))
                else:
                    if next_beam.dir == Dir.Left:
                        next_beam.x -= 1
                    elif next_beam.dir == Dir.Right:
                        next_beam.x += 1
                    else:
                        raise RuntimeError
                    beams.append(next_beam)

            elif tile == '/':
                if next_beam.dir == Dir.Right:
                    next_beam.y -= 1
                    next_beam.dir = Dir.Up
                elif next_beam.dir == Dir.Left:
                    next_beam.y += 1
                    next_beam.dir = Dir.Down
                elif next_beam.dir == Dir.Up:
                    next_beam.x += 1
                    next_beam.dir = Dir.Right
                elif next_beam.dir == Dir.Down:
                    next_beam.x -= 1
                    next_beam.dir = Dir.Left
                else:
                    raise RuntimeError
                beams.append(next_beam)

            elif tile == '\\':
                if next_beam.dir == Dir.Right:
                    next_beam.y += 1
                    next_beam.dir = Dir.Down
                elif next_beam.dir == Dir.Left:
                    next_beam.y -= 1
                    next_beam.dir = Dir.Up
                elif next_beam.dir == Dir.Up:
                    next_beam.x -= 1
                    next_beam.dir = Dir.Left
                elif next_beam.dir == Dir.Down:
                    next_beam.x += 1
                    next_beam.dir = Dir.Right
                else:
                    raise RuntimeError
                beams.append(next_beam)

            else:
                raise RuntimeError

        self.beams.clear()
        for next_beam in beams:
            if next_beam.y < 0 or next_beam.y == self.dy:
                continue
            if next_beam.x < 0 or next_beam.x == self.dx:
                continue
            self.beams.append(next_beam)

        print(np.sum(self.mask))


def load_input(filename: str) -> List[str]:

    with open(filename) as f:
        lines = [l for l in [l.strip() for l in f] if l]

    return lines


def part1(filename: str) -> Tuple[Field, int]:
    
    lines = load_input(filename)

    field = Field(lines, [Beam(0, 0, Dir.Right)])

    while len(field.beams) > 0:
        field.tick()

    total = np.sum(field.mask)

    return field, total


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

    field, answer1 = part1('day_16_input.txt')
    print(f"{answer1}")

    # answer2 = part2(steps)
    # print(f"{answer2}")

    return 0


if __name__ == '__main__':
    sys.exit(main())
