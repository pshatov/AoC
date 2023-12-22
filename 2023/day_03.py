import sys

from functools import reduce
from typing import List
from dataclasses import dataclass


@dataclass
class PartNumber:

    field: List[str]

    index_top: int
    index_left: int
    index_right: int

    def __repr__(self) -> str:
        return self.field[self.index_top][self.index_left : self.index_right + 1]
    
    @property
    def value(self) -> int:
        return int(str(self))


def load_input(filename: str) -> List[str]:

    with open(filename) as f:
        all_lines = [l for l in [l.strip() for l in f] if l]

    return all_lines


def check_partnumber_valid(field: List[str], pn: PartNumber) -> bool:
    
    y = pn.index_top
    for x in range(pn.index_left - 1, pn.index_right + 2):
        if x < 0 or x >= len(field[y]):
            continue
        if y - 1 >= 0 and field[y-1][x] != '.':
            return True
        if y + 1 < len(field) and field[y + 1][x] != '.':
            return True
        
    if pn.index_left - 1 >= 0 and field[y][pn.index_left - 1] != '.':
        return True
    
    if pn.index_right + 1 < len(field[y]) and field[y][pn.index_right + 1] != '.':
        return True

    return False


def part1(filename: str) -> int:

    field = load_input(filename)

    all_partnumbers = []
    for y in range(len(field)):
        field_line = field[y]
        
        start_index = -1
        line_partnumbers = []
        for index, char in enumerate(field_line + '.'):
            if start_index == -1:
                if str.isdigit(char):
                    start_index = index
            else:
                if not str.isdigit(char):
                    line_partnumbers.append(PartNumber(field, y, start_index, index - 1))
                    start_index = -1

        all_partnumbers += line_partnumbers

    sum = 0
    for next_partnumber in all_partnumbers:
        pn_valid = check_partnumber_valid(field, next_partnumber)
        if pn_valid:
            sum += next_partnumber.value

    return field, all_partnumbers, sum


def find_adjacent_partnumbers(y: int, x: int, all_partnumbers: List[PartNumber]) -> List[PartNumber]:

    adjacent_partnumbers = []
    for next_partnumber in all_partnumbers:
        if y == next_partnumber.index_top:
            if x == next_partnumber.index_left - 1 or x == next_partnumber.index_right + 1:
                adjacent_partnumbers.append(next_partnumber)
                continue
        if y == next_partnumber.index_top - 1 or y == next_partnumber.index_top + 1:
            if next_partnumber.index_left - 1 <= x <= next_partnumber.index_right + 1:
                adjacent_partnumbers.append(next_partnumber)
                continue

    return adjacent_partnumbers


def part2(field: List[str], all_partnumbers: List[PartNumber]) -> int:

    sum = 0
    for y in range(len(field)):
        for x in range(len(field[y])):
            if field[y][x] == '*':
                adjacent_partnumbers = find_adjacent_partnumbers(y, x, all_partnumbers)
                if len(adjacent_partnumbers) == 2:
                    ratio = reduce(lambda a, b: a * b, [pn.value for pn in adjacent_partnumbers])
                    sum += ratio

    return sum


def main() -> int:

    field, all_partnumbers, sum1 = part1('day_03_input.txt')
    sum2 = part2(field, all_partnumbers)

    print(f"{sum1}")
    print(f"{sum2}")

    return 0


if __name__ == '__main__':
    sys.exit(main())
