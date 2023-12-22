import sys
import numpy as np

from copy import deepcopy
from enum import Enum, auto
from dataclasses import dataclass, replace
from typing import Tuple, List, Dict, Optional


@dataclass
class Record:
    row: str
    counts: List[int]


def load_input(filename: str) -> List[Record]:

    with open(filename) as f:
        all_lines = [l for l in [l.strip() for l in f] if l]

    field = []
    for next_line in all_lines:
        row, counts = next_line.split(' ')
        field.append(Record(row, [int(c) for c in counts.split(',')]))

    return field


def validate_row(current_record: str, checksum_known: List[int]) -> int:

    checksum = []
    if current_record[0] == '#':
        checksum.append(1)

    for i in range(1, len(current_record)):
        ch = current_record[i]
        ch_prev = current_record[i - 1]
        if ch == '.':
            continue
        elif ch == '#':
            if ch_prev == '.':
                checksum.append(1)
            elif ch_prev == '#':
                checksum[-1] += 1
            else:
                raise RuntimeError

        else:
            raise RuntimeError
        
    if len(checksum) != len(checksum_known):
        return 0
    
    for i in range(len(checksum)):
        if checksum[i] != checksum_known[i]:
            return 0

    return 1


def bruteforce_record_recursive(current_record: str,
                                checksum: List[int],
                                current_total: List[int]) -> None:
    if '?' in current_record:
        for ch in ".#":
            bruteforce_record_recursive(
                current_record.replace('?', ch, 1),
                checksum,
                current_total)
    else:
        current_total[0] += validate_row(current_record, checksum)


def calc_num_variants(record: Record) -> int:
    current_total = [0]
    bruteforce_record_recursive(record.row, record.counts, current_total)
    return current_total[0]


def part1(filename: str) -> Tuple[List[Record], int]:
    
    field = load_input(filename)

    total = 0
    for i, next_record in enumerate(field):
        num_variants = calc_num_variants(next_record)
        print(f"{i + 1}: {num_variants}")
        total += num_variants

    return field, total


def part2(field: List[Record]) -> int:

    for next_record in field:
        next_record.row = '?'.join(5 * [next_record.row])
        next_record.counts *= 5

    total = 0
    for i, next_record in enumerate(field):
        num_variants = calc_num_variants(next_record)
        print(f"{i + 1}: {num_variants}")
        total += num_variants

    return field, total


def main() -> int:

    field, answer1 = part1('day_12_input.txt')
    answer2 = part2(field)

    print(f"{answer1}")
    print(f"{answer2}")

    return 0


if __name__ == '__main__':
    sys.exit(main())
