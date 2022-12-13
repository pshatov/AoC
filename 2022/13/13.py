# ---------------------------------------------------------------------------------------------------------------------
# 13.py
# ---------------------------------------------------------------------------------------------------------------------
# AoC '22
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------------------------------------------------
from typing import List, Optional, Union


# ---------------------------------------------------------------------------------------------------------------------
# New Types
# ---------------------------------------------------------------------------------------------------------------------
ListOrInt = Union[List, int]


# ---------------------------------------------------------------------------------------------------------------------
class Pair:

    # -----------------------------------------------------------------------------------------------------------------
    def __init__(self, left_part: str, right_part: str) -> None:
        self.left_part = eval(left_part)
        self.right_part = eval(right_part)
    # -----------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def str_no_spaces(value: ListOrInt) -> str:
    return str(value).replace(' ', '')
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def print_level(msg: str, level: int) -> None:
    print("%s- %s" % ("  " * level, msg))
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def compare_order(left_part: ListOrInt, right_part: ListOrInt, level: Optional[int] = 0) -> int:

    print_level("Compare %s vs %s" % (str_no_spaces(left_part), str_no_spaces(right_part)), level)

    if isinstance(left_part, int) and isinstance(right_part, int):
        if left_part < right_part:
            print_level("Left side is smaller, so inputs are in the right order", level + 1)
            return -1
        elif left_part == right_part:
            return 0
        else:
            print_level("Right side is smaller, so inputs are not in the right order", level + 1)
            return 1
    elif isinstance(left_part, list) and isinstance(right_part, list):
        index = 0
        while index < min(len(left_part), len(right_part)):
            correct_order = compare_order(left_part[index], right_part[index], level + 1)
            if correct_order != 0:
                return correct_order
            index += 1
        if len(left_part) < len(right_part):
            print_level("Left side ran out of items, so inputs are in the right order", level)
            return -1
        elif len(left_part) == len(right_part):
            return 0
        else:
            print_level("Right side ran out of items, so inputs are not in the right order", level)
            return 1
    elif isinstance(left_part, list) and isinstance(right_part, int):
        right_part = [right_part]
        print_level("Mixed types; convert right to %s and retry comparison" % str_no_spaces(right_part), level + 1)
        return compare_order(left_part, right_part)
    elif isinstance(left_part, int) and isinstance(right_part, list):
        left_part = [left_part]
        print_level("Mixed types; convert left to %s and retry comparison" % str_no_spaces(left_part), level + 1)
        return compare_order(left_part, right_part)
    else:
        raise RuntimeError
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def main() -> None:

    with open('input.txt') as file:
        all_lines = [line.strip() for line in file]

    while not all_lines[-1]:
        all_lines = all_lines[:-1]
    all_lines.append('')

    assert len(all_lines) % 3 == 0

    all_pairs = []
    for i in range(len(all_lines)):
        if i % 3 == 2:
            assert not all_lines[i]
            all_pairs.append(Pair(all_lines[i - 2], all_lines[i - 1]))

    result = 0
    for i in range(len(all_pairs)):
        i1 = i + 1
        print("== Pair %d ==" % i1)
        next_pair = all_pairs[i]
        correct_order = compare_order(next_pair.left_part, next_pair.right_part)
        if correct_order == -1:
            result += i1
    print("part 1: %d" % result)

    all_pairs.append(Pair("[[2]]", "[[6]]"))
    all_signals = []
    for next_pair in all_pairs:
        all_signals.append(next_pair.left_part)
        all_signals.append(next_pair.right_part)
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    main()
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
# End of File
# ---------------------------------------------------------------------------------------------------------------------
