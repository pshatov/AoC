# ---------------------------------------------------------------------------------------------------------------------
# 8.py
# ---------------------------------------------------------------------------------------------------------------------
# AoC '22
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------------------------------------------------
from typing import List


# ---------------------------------------------------------------------------------------------------------------------
# noinspection DuplicatedCode
def check_visible(forest: List[List[int]], tree_y: int, tree_x: int, forest_h: int, forest_w: int) -> bool:

    tree_z = forest[tree_y][tree_x]

    visible_top, visible_bottom = True, True
    for y in range(forest_h):
        if y < tree_y and forest[y][tree_x] >= tree_z:
            visible_top = False
        if y > tree_y and forest[y][tree_x] >= tree_z:
            visible_bottom = False

    visible_left, visible_right = True, True
    for x in range(forest_w):
        if x < tree_x and forest[tree_y][x] >= tree_z:
            visible_left = False
        if x > tree_x and forest[tree_y][x] >= tree_z:
            visible_right = False

    return visible_top or visible_bottom or visible_left or visible_right
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
# noinspection DuplicatedCode
def calc_score(forest: List[List[int]], tree_y: int, tree_x: int, forest_h: int, forest_w: int) -> int:

    tree_z = forest[tree_y][tree_x]

    score_top = 0
    for y in range(tree_y - 1, -1, -1):
        score_top += 1
        if forest[y][tree_x] >= tree_z:
            break

    score_bottom = 0
    for y in range(tree_y + 1, forest_h):
        score_bottom += 1
        if forest[y][tree_x] >= tree_z:
            break

    score_left = 0
    for x in range(tree_x - 1, -1, -1):
        score_left += 1
        if forest[tree_y][x] >= tree_z:
            break

    score_right = 0
    for x in range(tree_x + 1, forest_w):
        score_right += 1
        if forest[tree_y][x] >= tree_z:
            break

    return score_top * score_bottom * score_left * score_right
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def main() -> None:

    with open('input.txt') as file:
        all_lines = [line for line in [line.strip() for line in file] if line]

    forest = []
    height = len(all_lines)
    width = None
    for y in range(height):
        next_line = all_lines[y]
        if y == 0:
            width = len(next_line)
        elif len(next_line) != width:
            raise RuntimeError
        forest.append([int(t) for t in next_line])

    num_visible = 0
    for y in range(height):
        for x in range(width):
            if y == 0 or x == 0 or y == (height - 1) or x == (width - 1):
                num_visible += 1
            else:
                if check_visible(forest, y, x, height, width):
                    num_visible += 1

    print("part 1: %d" % num_visible)

    max_score = 0
    for y in range(1, height - 1):
        for x in range(1, width - 1):
            score = calc_score(forest, y, x, height, width)
            if score > max_score:
                max_score = score

    print("part 2: %d" % max_score)
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    main()
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
# End of File
# ---------------------------------------------------------------------------------------------------------------------
