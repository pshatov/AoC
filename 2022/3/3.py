# ---------------------------------------------------------------------------------------------------------------------
# 3.py
# ---------------------------------------------------------------------------------------------------------------------
# AoC '22
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------------------------------------------------
from typing import List


# ---------------------------------------------------------------------------------------------------------------------
def find_wrong_item_type(items: str) -> str:

    num_items = len(items)
    assert num_items % 2 == 0

    left_part = items[:num_items // 2]
    right_part = items[num_items // 2:]

    wrong_items = set(left_part).intersection(set(right_part))
    assert len(wrong_items) == 1

    return list(wrong_items)[0]
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def find_common_item_type(items: List[str]) -> str:

    items_x = set(items[0])
    items_y = set(items[1])
    items_z = set(items[2])

    common_items = items_x.intersection(items_y).intersection(items_z)
    assert len(common_items) == 1

    return list(common_items)[0]
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def get_item_type_priority(item_type: str) -> int:
    assert len(item_type) == 1
    assert str.isalpha(item_type)
    if str.islower(item_type):
        ord_offset = ord('a') - 1
    else:
        ord_offset = ord('A') - 27

    return ord(item_type) - ord_offset
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def main() -> None:

    with open('input.txt') as file:
        all_lines = [line for line in [line.strip() for line in file.readlines()] if line]

    total_priority = 0
    for next_line in all_lines:
        wrong_type = find_wrong_item_type(next_line)
        wrong_type_priority = get_item_type_priority(wrong_type)
        total_priority += wrong_type_priority
    print("part 1: %d" % total_priority)

    assert len(all_lines) % 3 == 0

    total_priority = 0
    for i in range(0, len(all_lines), 3):
        common_type = find_common_item_type(all_lines[i: i + 3])
        common_type_priority = get_item_type_priority(common_type)
        total_priority += common_type_priority
    print("part 2: %d" % total_priority)
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    main()
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
# End of File
# ---------------------------------------------------------------------------------------------------------------------
