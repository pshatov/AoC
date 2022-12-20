# ---------------------------------------------------------------------------------------------------------------------
# 15.py
# ---------------------------------------------------------------------------------------------------------------------
# AoC '22
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
# TODO: Very slow, needs rewrite!
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------------------------------------------------
import re


# ---------------------------------------------------------------------------------------------------------------------
# More Imports
# ---------------------------------------------------------------------------------------------------------------------
from typing import List, Optional


# ---------------------------------------------------------------------------------------------------------------------
class Range:

    # -----------------------------------------------------------------------------------------------------------------
    def __init__(self, begin: int, end: int) -> None:
        assert begin <= end
        self.begin, self.end = begin, end
        self.active = True
        self.stack_begin, self.stack_end = None, None
    # -----------------------------------------------------------------------------------------------------------------

    # -----------------------------------------------------------------------------------------------------------------
    @property
    def length(self) -> int:
        return self.end - self.begin + 1
    # -----------------------------------------------------------------------------------------------------------------

    # -----------------------------------------------------------------------------------------------------------------
    def __repr__(self) -> str:
        return "<%d..%d>" % (self.begin, self.end)
    # -----------------------------------------------------------------------------------------------------------------

    # -----------------------------------------------------------------------------------------------------------------
    def does_overlap(self, other_range: 'Range') -> bool:
        return not (self.begin > other_range.end or other_range.begin > self.end)
    # -----------------------------------------------------------------------------------------------------------------

    # -----------------------------------------------------------------------------------------------------------------
    def combine(self, other_range: 'Range') -> None:
        if other_range.begin < self.begin:
            self.begin = other_range.begin
        if other_range.end > self.end:
            self.end = other_range.end
        other_range.active = False
    # -----------------------------------------------------------------------------------------------------------------

    # -----------------------------------------------------------------------------------------------------------------
    def push(self) -> None:
        assert self.stack_begin is None and self.stack_end is None
        self.stack_begin, self.stack_end = self.begin, self.end
    # -----------------------------------------------------------------------------------------------------------------

    # -----------------------------------------------------------------------------------------------------------------
    def pop(self) -> None:
        assert self.stack_begin is not None and self.stack_end is not None
        self.begin, self.end = self.stack_begin, self.stack_end
        self.stack_begin, self.stack_end = None, None
    # -----------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
class XY:

    # -----------------------------------------------------------------------------------------------------------------
    def __init__(self, x: int, y: int) -> None:
        self.x, self.y = x, y
    # -----------------------------------------------------------------------------------------------------------------

    # -----------------------------------------------------------------------------------------------------------------
    def __repr__(self) -> str:
        return "<%d,%d>" % (self.x, self.y)
    # -----------------------------------------------------------------------------------------------------------------

    # -----------------------------------------------------------------------------------------------------------------
    def __eq__(self, other: 'XY') -> bool:
        return self.x == other.x and self.y == other.y
    # -----------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
class Sensor:

    InputRegExp = re.compile("^Sensor at x=(-?\\d+), y=(-?\\d+): closest beacon is at x=(-?\\d+), y=(-?\\d+)$")

    # -----------------------------------------------------------------------------------------------------------------
    def __init__(self, input_line: str) -> None:

        m = Sensor.InputRegExp.fullmatch(input_line)
        assert m is not None

        self.own_xy = XY(int(m.group(1)), int(m.group(2)))
        self.beacon_xy = XY(int(m.group(3)), int(m.group(4)))

        dx = self.beacon_xy.x - self.own_xy.x
        dy = self.beacon_xy.y - self.own_xy.y

        self.dist = abs(dx) + abs(dy)

        self.y_top = self.own_xy.y + self.dist
        self.y_bot = self.own_xy.y - self.dist
    # -----------------------------------------------------------------------------------------------------------------

    # -----------------------------------------------------------------------------------------------------------------
    def __repr__(self) -> str:
        return "@%s -> %s (%d)" % (str(self.own_xy), str(self.beacon_xy), self.dist)
    # -----------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def combine_ranges(all_ranges: List[Range]) -> None:

    keep_combining = True
    while keep_combining:
        keep_combining = False
        for i in range(len(all_ranges)):
            if all_ranges[i] is None or not all_ranges[i].active:
                continue
            for j in range(i + 1, len(all_ranges)):
                if all_ranges[j] is None or not all_ranges[j].active:
                    continue
                if all_ranges[i].does_overlap(all_ranges[j]):
                    keep_combining = True
                    all_ranges[i].combine(all_ranges[j])
                    break
            if keep_combining:
                break

    keep_combining = True
    while keep_combining:
        keep_combining = False
        for i in range(len(all_ranges)):
            if all_ranges[i] is None or not all_ranges[i].active:
                continue
            for j in range(i + 1, len(all_ranges)):
                if all_ranges[j] is None or not all_ranges[j].active:
                    continue
                if all_ranges[i].end + 1 == all_ranges[j].begin:
                    keep_combining = True
                    all_ranges[i].end = all_ranges[j].end
                    all_ranges[j].active = False
                    break
                elif all_ranges[i].begin - 1 == all_ranges[j].end:
                    keep_combining = True
                    all_ranges[i].begin = all_ranges[j].begin
                    all_ranges[j].active = False
                    break
            if keep_combining:
                break
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def main() -> None:

    with open('input.txt') as file:
        all_lines = [line for line in [line.strip() for line in file] if line]

    all_sensors = [Sensor(next_line) for next_line in all_lines]

    factor = 4000000
    # y_target, y_limit = 10, 40
    y_target, y_limit = 2000000, 4000000

    all_ranges: List[Optional[Range]]
    all_ranges = []
    for i in range(len(all_sensors)):
        all_ranges.append(None)

    for y in range(y_limit + 1):
        for i in range(len(all_ranges)):
            if all_ranges[i] is None:
                if all_sensors[i].y_bot <= y <= all_sensors[i].y_top:
                    x_delta = all_sensors[i].dist - abs(all_sensors[i].own_xy.y - y)
                    x_left = all_sensors[i].own_xy.x - x_delta
                    x_right = all_sensors[i].own_xy.x + x_delta
                    all_ranges[i] = Range(x_left, x_right)
            else:
                all_ranges[i].pop()
                all_ranges[i].active = True
                if y > all_sensors[i].y_top:
                    assert all_ranges[i].begin == all_ranges[i].end
                    all_ranges[i] = None
                elif y <= all_sensors[i].own_xy.y:
                    all_ranges[i].begin -= 1
                    all_ranges[i].end += 1
                else:
                    all_ranges[i].begin += 1
                    all_ranges[i].end -= 1

        for i in range(len(all_ranges)):
            if all_ranges[i] is not None:
                all_ranges[i].push()

        combine_ranges(all_ranges)

        if y == y_target:
            total_length = 0
            removed_beacon_x = []
            for ar in all_ranges:
                if ar is not None and ar.active:
                    total_length += ar.length
            for next_sensor in all_sensors:
                if next_sensor.beacon_xy.y == y_target:
                    if next_sensor.beacon_xy.x not in removed_beacon_x:
                        total_length -= 1
                        removed_beacon_x.append(next_sensor.beacon_xy.x)
            print("part 1: %d" % total_length)

        num_active_ranges = 0
        for i in range(len(all_ranges)):
            if all_ranges[i] is not None and all_ranges[i].active:
                num_active_ranges += 1

        if num_active_ranges > 1:
            assert num_active_ranges == 2
            active_ranges = []
            for i in range(len(all_ranges)):
                if all_ranges[i] is not None and all_ranges[i].active:
                    active_ranges.append(all_ranges[i])

            assert active_ranges[0].end == active_ranges[1].begin - 2
            print("part 2: %d" % ((active_ranges[0].end + 1) * factor + y))
            break
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    main()
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
# End of File
# ---------------------------------------------------------------------------------------------------------------------
