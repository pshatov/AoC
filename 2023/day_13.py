import sys
import numpy as np

from functools import reduce
from numpy import ndarray
from typing import Tuple, List, Dict, Optional


class Field:

    dy: int
    dx: int
    matrix: ndarray
    axes_vertical_by_row: List[List[int]]
    axes_horizontal_by_column: List[List[int]]

    def __init__(self, lines: List[str]) -> None:

        self.dy = len(lines)
        self.dx = len(lines[0])
        shape = self.dy, self.dx

        self.matrix = np.zeros(shape, dtype=np.int_)
        for y in range(self.dy):
            for x in range(self.dx):
                if lines[y][x] == "#":
                    self.matrix[y, x] = 1

        self.axes_vertical_by_row = []
        self.axes_horizontal_by_column = []

        for y in range(self.dy):
            self.axes_vertical_by_row.append([])

        for x in range(self.dx):
            self.axes_horizontal_by_column.append([])

    def find_vertical_axes(self) -> None:

        for y in range(self.dy):
            for x in range(1, self.dx):
                if self.is_vertical_axis(y, x):
                    self.axes_vertical_by_row[y].append(x)

    def find_horizontal_axes(self) -> None:
        for x in range(self.dx):
            for y in range(1, self.dy):
                if self.is_horizontal_axis(y, x):
                    self.axes_horizontal_by_column[x].append(y)

    def is_vertical_axis(self, y: int, x: int) -> bool:

        left_range = iter(range(x - 1, -1, -1))
        right_range = iter(range(x, self.dx))
        while True:
            try:
                x_left = next(left_range)
                x_right = next(right_range)
            except StopIteration:
                break
            if self.matrix[y, x_left] != self.matrix[y, x_right]:
                return False

        return True

    def is_horizontal_axis(self, y: int, x: int) -> bool:

        up_range = iter(range(y - 1, -1, -1))
        down_range = iter(range(y, self.dy))
        while True:
            try:
                y_up = next(up_range)
                y_down = next(down_range)
            except StopIteration:
                break
            if self.matrix[y_up, x] != self.matrix[y_down, x]:
                return False

        return True


def load_input(filename: str) -> List[Field]:

    with open(filename) as f:
        all_lines = [l.strip() for l in f]

    assert all_lines[0] != ""

    while all_lines[-1] == "":
        del all_lines[-1]
    all_lines.append("")

    fields = []
    some_lines = []
    for next_line in all_lines:
        if next_line != "":
            some_lines.append(next_line)
        else:
            fields.append(Field(some_lines))
            some_lines.clear()

    return fields


def part1(filename: str) -> Tuple[List[ndarray], int]:
    
    fields = load_input(filename)

    for next_field in fields:
        next_field.find_vertical_axes()
        next_field.find_horizontal_axes()

    total_vertical = 0
    total_horizontal = 0

    for next_field in fields:
        v = reduce(lambda a, b: set(a) & set(b), next_field.axes_vertical_by_row)
        h = reduce(lambda a, b: set(a) & set(b), next_field.axes_horizontal_by_column)
        assert len(v) + len(h) == 1
        total_vertical += sum(v)
        total_horizontal += sum(h)

    total = total_vertical + 100 * total_horizontal

    return fields, total


def part2(fields: List[Field]) -> int:

    total_vertical = 0
    total_horizontal = 0

    for next_field in fields:
        
        vertical_counts = {}
        for next_row in next_field.axes_vertical_by_row:
            for x in next_row:
                if x not in vertical_counts:
                    vertical_counts[x] = 0
                vertical_counts[x] += 1

        horizontal_counts = {}
        for next_column in next_field.axes_horizontal_by_column:
            for y in next_column:
                if y not in horizontal_counts:
                    horizontal_counts[y] = 0
                horizontal_counts[y] += 1

        v = [x for x in vertical_counts if vertical_counts[x] == next_field.dy - 1]            
        h = [y for y in horizontal_counts if horizontal_counts[y] == next_field.dx - 1]

        assert len(h) + len(v) == 1

        total_vertical += sum(v)
        total_horizontal += sum(h)

    total = total_vertical + 100 * total_horizontal

    return total


def main() -> int:

    fields, answer1 = part1('day_13_input.txt')
    answer2 = part2(fields)

    print(f"{answer1}")
    print(f"{answer2}")

    return 0


if __name__ == '__main__':
    sys.exit(main())
