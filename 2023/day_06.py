import sys

from math import sqrt, ceil, floor
from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class Record:
    time: int
    distance: int


def load_input(filename: str) -> List[Record]:

    with open(filename) as f:
        time_line = f.readline()
        distance_line = f.readline()

    time_line_parts = tuple(t for t in time_line.split(':'))
    distance_line_parts = tuple(d for d in distance_line.split(':'))

    assert len(time_line_parts) == 2
    assert len(distance_line_parts) == 2

    assert time_line_parts[0] == "Time"
    assert distance_line_parts[0] == "Distance"

    times = [int(t) for t in time_line_parts[1].split(' ') if t]
    distances = [int(d) for d in distance_line_parts[1].split(' ') if d]
    assert len(times) == len(distances)

    records = [Record(times[i], distances[i]) for i in range(len(times))]
    
    return records


def calc_multipier(record: Record) -> int:

    d = record.time ** 2 - 4 * record.distance
    assert d > 0
    t1 = ceil(0.5 * (record.time - sqrt(d)))
    t2 = floor(0.5 * (record.time + sqrt(d)))

    if record.time * t1 - t1 ** 2 == record.distance:
        t1 += 1

    if record.time * t2 - t2 ** 2 == record.distance:
        t2 -= 1

    return t2 - t1 + 1


def part1(filename: str) -> Tuple[List[Record], int]:
    
    all_records = load_input(filename)

    product = 1
    for next_record in all_records:
        product *= calc_multipier(next_record)

    return all_records, product


def part2(all_records: List[Record]) -> int:
    final_time = int(''.join([str(r.time) for r in all_records]))
    final_distance = int(''.join([str(r.distance) for r in all_records]))
    return calc_multipier(Record(final_time, final_distance))


def main() -> int:

    all_records, answer1 = part1('day_06_input.txt')
    answer2 = part2(all_records)

    print(f"{answer1}")
    print(f"{answer2}")

    return 0


if __name__ == '__main__':
    sys.exit(main())
