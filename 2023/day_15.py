import sys

from dataclasses import dataclass
from typing import Tuple, List, Dict, Optional


@dataclass
class Lens:
    label: str
    power: int


def load_input(filename: str) -> List[str]:

    with open(filename) as f:
        line = f.readline()

    steps = line.split(',')

    return steps


def aoc_hash(s: str) -> int:
    v = 0
    for c in s:
        v += ord(c)
        v *= 17
        v &= 0xff
    return v


def part1(filename: str) -> Tuple[List[str], int]:
    
    all_steps = load_input(filename)

    total = 0
    for next_step in all_steps:
        t = aoc_hash(next_step)
        # print(f"{next_step}: {t}")
        total += t

    return all_steps, total


def part2(steps: List[str]) -> int:

    lens_by_box: List[List[Lens]] = []
    for i in range(256):
        lens_by_box.append([])

    for next_step in steps:
        label = ""
        for i in range(len(next_step)):
            if not next_step[i].isalpha():
                break
        label = next_step[:i]
        box_index = aoc_hash(label)
        op = next_step[i]
        box = lens_by_box[box_index]
        if op == '-':
            remove_index = -1
            for i, lens in enumerate(box):
                if lens.label == label:
                    remove_index = i
                    break
            if remove_index != -1:
                del box[remove_index]
        elif op == '=':
            power = int(next_step[i + 1:])
            replace_index = -1
            for i, lens in enumerate(box):
                if lens.label == label:
                    replace_index = i
                    break
            if replace_index != -1:
                box[replace_index] = Lens(label, power)
            else:
                box.append(Lens(label, power))
        else:
            raise RuntimeError

        if False:
            print(f'After "{next_step}":')
            for i, box in enumerate(lens_by_box):
                if len(box) > 0:
                    print(f'Box {i}:', end='')
                    for lens in box:
                        print(f' [{lens.label} {lens.power}]', end='')
                    print('\n')

    total = 0
    for i, box in enumerate(lens_by_box):
        for j, lens in enumerate(box):
            power = (i + 1) * (j + 1) * lens.power
            total += power

    return total


def main() -> int:

    steps, answer1 = part1('day_15_input.txt')
    print(f"{answer1}")

    answer2 = part2(steps)
    print(f"{answer2}")

    return 0


if __name__ == '__main__':
    sys.exit(main())
