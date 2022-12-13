# ---------------------------------------------------------------------------------------------------------------------
# 13.py
# ---------------------------------------------------------------------------------------------------------------------
# AoC '22
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------------------------------------------------
from functools import cmp_to_key


# ---------------------------------------------------------------------------------------------------------------------
# More Imports
# ---------------------------------------------------------------------------------------------------------------------
from typing import Union, List


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
def compare_order(left_part: ListOrInt, right_part: ListOrInt) -> int:

    if isinstance(left_part, int) and isinstance(right_part, int):
        if left_part < right_part:
            return -1
        elif left_part == right_part:
            return 0
        else:
            return 1
    elif isinstance(left_part, list) and isinstance(right_part, list):
        index = 0
        while index < min(len(left_part), len(right_part)):
            correct_order = compare_order(left_part[index], right_part[index])
            if correct_order != 0:
                return correct_order
            index += 1
        if len(left_part) < len(right_part):
            return -1
        elif len(left_part) == len(right_part):
            return 0
        else:
            return 1
    elif isinstance(left_part, list) and isinstance(right_part, int):
        right_part = [right_part]
        return compare_order(left_part, right_part)
    elif isinstance(left_part, int) and isinstance(right_part, list):
        left_part = [left_part]
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

    all_signals_sorted = sorted(all_signals, key=cmp_to_key(compare_order))
    index, index_divider_2, index_divider_6 = 1, None, None
    for next_signal in all_signals_sorted:
        if len(next_signal) == 1:
            if isinstance(next_signal[0], list):
                if len(next_signal[0]) == 1:
                    if isinstance(next_signal[0][0], int):
                        if next_signal[0][0] == 2:
                            index_divider_2 = index
                        elif next_signal[0][0] == 6:
                            index_divider_6 = index
        index += 1

    assert index_divider_2 is not None
    assert index_divider_6 is not None

    print("part 2: %d" % (index_divider_2 * index_divider_6))
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    main()
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
# End of File
# ---------------------------------------------------------------------------------------------------------------------
