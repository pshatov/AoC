import sys
import numpy as np

from typing import Tuple, List, Dict, Optional


def load_input(filename: str) -> List[List[int]]:

    with open(filename) as f:
        all_lines = [l for l in [l.strip() for l in f] if l]

    all_seqs = []
    for next_line in all_lines:
        all_seqs.append([int(t) for t in next_line.split(' ')])
        
    return all_seqs


def extrapolate_forward(seq_input: List[int]) -> int:

    seqs_temp = [seq_input]

    reduce = True
    while reduce:
        seq_next = []
        for i in range(1, len(seqs_temp[-1])):
            seq_next.append(seqs_temp[-1][i] - seqs_temp[-1][i - 1])
        seqs_temp.append(seq_next)
        reduce = min(seq_next) != 0 or max(seq_next) != 0

    for i in range(len(seqs_temp) - 2, -1, -1):
        seqs_temp[i].append(seqs_temp[i][-1] + seqs_temp[i + 1][-1])

    return seqs_temp[0][-1]


def extrapolate_backward(seq_input: List[int]) -> int:

    seqs_temp = [seq_input.copy()]

    reduce = True
    while reduce:
        seq_next = []
        for i in range(1, len(seqs_temp[-1])):
            seq_next.append(seqs_temp[-1][i] - seqs_temp[-1][i - 1])
        seqs_temp.append(seq_next)
        reduce = min(seq_next) != 0 or max(seq_next) != 0

    for i in range(len(seqs_temp) - 2, -1, -1):
        seqs_temp[i].insert(0, seqs_temp[i][0] - seqs_temp[i + 1][0])

    return seqs_temp[0][0]


def part1(filename: str) -> Tuple[List[List[int]], int]:
    all_seqs = load_input(filename)

    total = 0
    for next_seq in all_seqs:
        total += extrapolate_forward(next_seq)

    return all_seqs, total


def part2(all_seqs: List[List[int]]) -> int:

    total = 0
    for next_seq in all_seqs:
        total += extrapolate_backward(next_seq)

    return total


def main() -> int:

    all_seqs, answer1 = part1('day_09_input.txt')
    answer2 = part2(all_seqs)

    print(f"{answer1}")
    print(f"{answer2}")

    return 0


if __name__ == '__main__':
    sys.exit(main())
