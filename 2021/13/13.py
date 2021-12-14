# ---------------------------------------------------------------------------------------------------------------------
# AoC 2021
# ---------------------------------------------------------------------------------------------------------------------
# 13.py
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
# More Imports
# ---------------------------------------------------------------------------------------------------------------------
from typing import Tuple, List, Dict


# ---------------------------------------------------------------------------------------------------------------------
# Types
# ---------------------------------------------------------------------------------------------------------------------
DotXY = Tuple[int, int]
Paper = List[List[bool]]


# ---------------------------------------------------------------------------------------------------------------------
def fold_paper(paper: Paper, f: str) -> None:
    f = f[len('fold along '):]

    coord = int(f[2:])
    if f.startswith('x='):
        _fold_paper_along_x(paper, coord)
    elif f.startswith('y='):
        _fold_paper_along_y(paper, coord)
    else:
        raise RuntimeError
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def _fold_paper_along_x(paper: Paper, fold_x: int) -> None:

    new_paper: List[Dict[int, bool]]
    new_paper = []

    for y in range(len(paper)):

        new_paper.append(dict())

        for x in range(fold_x):
            new_paper[-1][x] = paper[y][x]

        for x in range(fold_x + 1, len(paper[y])):
            x_new = 2 * fold_x - x
            new_paper[-1][x_new] = paper[y][x] or new_paper[-1][x_new] if x_new in new_paper[-1].keys() else False

    for y in range(len(paper)):
        paper[y].clear()
        for x in sorted(new_paper[y].keys()):
            paper[y].append(new_paper[y][x])
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def _fold_paper_along_y(paper: Paper, fold_y: int) -> None:

    new_paper: Dict[int, List[bool]]
    new_paper = {}

    for y in range(fold_y):
        new_paper[y] = paper[y][:]

    for y in range(fold_y + 1, len(paper)):
        y_new = 2 * fold_y - y
        if y_new not in new_paper.keys():
            new_paper[y_new] = paper[y][:]
        else:
            for x in range(len(paper[y])):
                new_paper[y_new][x] = new_paper[y_new][x] or paper[y][x]

    paper.clear()
    for y in sorted(new_paper.keys()):
        paper.append(new_paper[y][:])
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def print_line() -> None:
    for x in range(8):
        if x == 0:
            print('+', end='')
        for xx in range(5):
            print('-', end='')
        print('+', end='')
    print()
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def print_paper(paper: Paper, y: int) -> None:
    for x in range(8):
        if x == 0:
            print('|', end='')
        for xx in range(5):
            print('X' if paper[y][5 * x + xx] else ' ', end='')
        print('|', end='')
    print()
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def main() -> None:

    with open('input.txt') as f:
        f_lines = [t.strip() for t in f.readlines()]

    i, dots = 0, []
    while len(f_lines[i]) > 0:
        dots.append(tuple(int(t) for t in f_lines[i].split(',')))
        i += 1

    i, folds = i + 1, []
    while i < len(f_lines):
        folds.append(f_lines[i])
        i += 1

    x_max = max(t[0] for t in dots)
    y_max = max(t[1] for t in dots)

    paper: Paper
    paper = []
    for y in range(y_max + 1):
        paper.append([False] * (x_max + 1))

    for dx, dy in dots:
        paper[dy][dx] = True

    fold_paper(paper, folds[0])
    num_dots = sum(sum(t) for t in paper)
    print("part 1: %d" % num_dots)

    for f in range(1, len(folds)):
        fold_paper(paper, folds[f])

    print("part 2:")
    print_line()
    for y in range(len(paper)):
        print_paper(paper, y)
    print_line()
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    main()
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
# End of File
# ---------------------------------------------------------------------------------------------------------------------
