import sys
import numpy as np

from copy import deepcopy
from enum import Enum, auto
from dataclasses import dataclass, replace
from typing import Tuple, List, Dict, Optional


FACTOR = 1000000


@dataclass
class XY:
    x: int
    y: int


def load_input(filename: str) -> np.ndarray:

    with open(filename) as f:
        all_lines = [l for l in [l.strip() for l in f] if l]

    shape = len(all_lines), len(all_lines[0])
    universe = np.zeros(shape, dtype=np.int_)

    dy, dx = shape
    for y in range(dy):
        for x in range(dx):
            if all_lines[y][x] == '#':
                universe[y, x] = 1

    return universe


def expand(universe: np.ndarray) -> np.ndarray:

    assert np.sum(universe[ :,  0] > 0)
    assert np.sum(universe[ :, -1] > 0)
    assert np.sum(universe[ 0,  :] > 0)
    assert np.sum(universe[-1,  :] > 0)

    y = 0
    h_shape = 1, universe.shape[1]
    h_line = np.full(h_shape, FACTOR, dtype=np.int_)
    while y < universe.shape[0]:
        if np.sum(universe[y, :]) % FACTOR == 0:
            a = universe[:y, :]
            b = h_line
            c = universe[y:, :]
            universe = np.vstack([a, b, c])
            y += 1
        y += 1

    x = 0
    v_shape = universe.shape[0], 1
    v_line = np.full(v_shape, FACTOR, dtype=np.int_)
    while x < universe.shape[1]:
        if np.sum(universe[:, x]) % FACTOR == 0:
            a = universe[:, :x]
            b = v_line
            c = universe[:, x:]
            universe = np.hstack([a, b, c])
            x += 1
        x += 1

    return universe


def find_galaxies(universe: np.ndarray) -> List[XY]:
    
    galaxies = []
    dy, dx = universe.shape
    for y in range(dy):
        for x in range(dx):
            if universe[y, x] == 1:
                galaxies.append(XY(x, y))

    return galaxies


def part1(filename: str) -> Tuple[np.ndarray, List[int], List[int], int]:
    
    universe = load_input(filename)
    universe = expand(universe)

    galaxies = find_galaxies(universe)

    total = 0
    for i in range(len(galaxies) - 1):
        for j in range(i + 1, len(galaxies)):
            dx = np.abs(galaxies[i].x - galaxies[j].x)
            dy = np.abs(galaxies[i].y - galaxies[j].y)
            total += dx + dy

    return universe, galaxies, total


def part2(universe: np.ndarray, galaxies: List[XY]) -> int:

    total = 0
    for i in range(len(galaxies) - 1):
        for j in range(i + 1, len(galaxies)):
            xx = galaxies[i].x, galaxies[j].x
            yy = galaxies[i].y, galaxies[j].y

            x1, x2 = min(xx), max(xx)
            y1, y2 = min(yy), max(yy)

            for y in range(y1, y2):
                if universe[y, 0] == FACTOR:
                    total += FACTOR - 1
                else:
                    total += 1

            for x in range(x1, x2):
                if universe[0, x] == FACTOR:
                    total += FACTOR - 1
                else:
                    total += 1

    return total


def main() -> int:

    universe, galaxies, answer1 = part1('day_11_input.txt')
    answer2 = part2(universe, galaxies)

    print(f"{answer1}")
    print(f"{answer2}")

    return 0


if __name__ == '__main__':
    sys.exit(main())
