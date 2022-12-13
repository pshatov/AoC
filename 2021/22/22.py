# ---------------------------------------------------------------------------------------------------------------------
# AoC 2021
# ---------------------------------------------------------------------------------------------------------------------
# 22.py
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------------------------------------------------
import re
import numpy as np


# ---------------------------------------------------------------------------------------------------------------------
# More Imports
# ---------------------------------------------------------------------------------------------------------------------
from enum import Enum
from typing import List, Optional, Tuple


# ---------------------------------------------------------------------------------------------------------------------
# Settings
# ---------------------------------------------------------------------------------------------------------------------
REGION_SIZE = 50
REACTOR_SIZE = 2 * REGION_SIZE + 1


# ---------------------------------------------------------------------------------------------------------------------
class ActionEnum(str, Enum):
    On = 'on'
    Off = 'off'
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
class Segment:

    begin: int
    end: int

    # -----------------------------------------------------------------------------------------------------------------
    def __init__(self, begin: int, end: int) -> None:
        assert begin <= end
        self.begin, self.end = begin, end
    # -----------------------------------------------------------------------------------------------------------------

    # -----------------------------------------------------------------------------------------------------------------
    def __repr__(self) -> str:
        return "%d..%d" % (self.begin, self.end)
    # -----------------------------------------------------------------------------------------------------------------

    # -----------------------------------------------------------------------------------------------------------------
    def range(self) -> range:
        return range(self.begin, self.end + 1)
    # -----------------------------------------------------------------------------------------------------------------

    # -----------------------------------------------------------------------------------------------------------------
    @property
    def length(self) -> int:
        return self.end - self.begin + 1
    # -----------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
class Cuboid:

    action: bool

    x_seg: Segment
    y_seg: Segment
    z_seg: Segment

    RE_CUBOID = re.compile(r"x=(-?\d+)\.\.(-?\d+),y=(-?\d+)\.\.(-?\d+),z=(-?\d+)\.\.(-?\d+)")

    ActionLUT = {ActionEnum.On: True,
                 ActionEnum.Off: False}

    # -----------------------------------------------------------------------------------------------------------------
    def __init__(self, s: str) -> None:

        m = None
        for a in list(ActionEnum):
            if s.startswith(a):
                m = self.RE_CUBOID.fullmatch(s[len(a) + 1:])
                self.action = Cuboid.ActionLUT[a]
                break

        if m is None:
            raise RuntimeError

        self.x_seg = Segment(int(m.group(1)), int(m.group(2)))
        self.y_seg = Segment(int(m.group(3)), int(m.group(4)))
        self.z_seg = Segment(int(m.group(5)), int(m.group(6)))
    # -----------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
class SimpleRectangle:

    x_seg: Segment
    y_seg: Segment

    # -----------------------------------------------------------------------------------------------------------------
    def __init__(self, x: Segment, y: Segment) -> None:
        self.x_seg, self.y_seg = x, y
    # -----------------------------------------------------------------------------------------------------------------

    # -----------------------------------------------------------------------------------------------------------------
    def __repr__(self) -> str:
        return "<x:%s, y:%s>" % (self.x_seg, self.y_seg)
    # -----------------------------------------------------------------------------------------------------------------

    # -----------------------------------------------------------------------------------------------------------------
    @property
    def area(self) -> int:
        return self.x_seg.length * self.y_seg.length
    # -----------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def get_overlapping_segment(a: Segment, b: Segment) -> Optional[Segment]:

    ab_left = max(a.begin, b.begin)
    ab_right = min(a.end, b.end)

    return Segment(ab_left, ab_right)
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def get_nonoverlapping_part(segment: Segment, overlap: Segment) -> List[Segment]:

    left_segment = Segment(segment.begin, overlap.begin - 1) if overlap.begin > segment.begin else None
    right_segment = Segment(overlap.end + 1, segment.end) if overlap.end < segment.end else None

    left_part = [left_segment] if left_segment else []
    right_part = [right_segment] if right_segment else []

    return left_part + right_part
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def check_overlap(seg1: Segment, seg2: Segment) -> bool:
    return seg1.begin <= seg2.end and seg1.end >= seg2.begin
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def part1(cuboids: List[Cuboid]) -> int:

    reactor_segment = Segment(-REGION_SIZE, REGION_SIZE)
    reactor = np.zeros([REACTOR_SIZE, REACTOR_SIZE, REACTOR_SIZE], dtype=np.int_)

    for i in range(len(cuboids)):

        ci = cuboids[i]

        if not check_overlap(reactor_segment, ci.x_seg):
            continue
        else:
            overlap_x = get_overlapping_segment(reactor_segment, ci.x_seg)

        if not check_overlap(reactor_segment, ci.y_seg):
            continue
        else:
            overlap_y = get_overlapping_segment(reactor_segment, ci.y_seg)

        if not check_overlap(reactor_segment, ci.z_seg):
            continue
        else:
            overlap_z = get_overlapping_segment(reactor_segment, ci.z_seg)

        new_value = 1 if ci.action else 0

        for x in overlap_x.range():
            for y in overlap_y.range():
                for z in overlap_z.range():
                    reactor[z + REGION_SIZE][y + REGION_SIZE][x + REGION_SIZE] = new_value

    return int(np.sum(reactor))
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def update_seg_min_max(seg: Segment, seg_min: Optional[int] = None, seg_max: Optional[int] = None) -> Tuple[int, int]:

    seg_min_new = seg.begin if seg_min is None else min(seg_min, seg.begin)
    seg_max_new = seg.end if seg_max is None else max(seg_max, seg.end)

    return seg_min_new, seg_max_new
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
# noinspection DuplicatedCode
def compute_pending_activation(new_rect: SimpleRectangle,
                               overlap_x: Segment, overlap_y: Segment) -> List[SimpleRectangle]:

    nooverlap_new_x = get_nonoverlapping_part(new_rect.x_seg, overlap_x)
    nooverlap_new_y = get_nonoverlapping_part(new_rect.y_seg, overlap_y)

    pending_rects = []
    for yy in nooverlap_new_y:
        for xx in nooverlap_new_x:
            pending_rects.append(SimpleRectangle(xx, yy))

    for yy in nooverlap_new_y:
        pending_rects.append(SimpleRectangle(overlap_x, yy))

    for xx in nooverlap_new_x:
        pending_rects.append(SimpleRectangle(xx, overlap_y))

    return pending_rects
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
# noinspection DuplicatedCode
def compute_remaining_active(active_rect: SimpleRectangle,
                             overlap_x: Segment, overlap_y: Segment) -> List[SimpleRectangle]:

    nooverlap_new_x = get_nonoverlapping_part(active_rect.x_seg, overlap_x)
    nooverlap_new_y = get_nonoverlapping_part(active_rect.y_seg, overlap_y)

    pending_rects = []
    for pending_y in nooverlap_new_y:
        for pending_x in nooverlap_new_x:
            pending_rects.append(SimpleRectangle(pending_x, pending_y))

    for yy in nooverlap_new_y:
        pending_rects.append(SimpleRectangle(overlap_x, yy))

    for xx in nooverlap_new_x:
        pending_rects.append(SimpleRectangle(xx, overlap_y))

    return pending_rects
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def rectangle_activate(active_rectangles: List[SimpleRectangle],
                       new_rectangle: SimpleRectangle) -> None:

    pending_rectangles = None
    for i in range(len(active_rectangles)):
        ari = active_rectangles[i]

        if not check_overlap(ari.x_seg, new_rectangle.x_seg):
            continue
        else:
            overlap_x = get_overlapping_segment(ari.x_seg, new_rectangle.x_seg)

        if not check_overlap(ari.y_seg, new_rectangle.y_seg):
            continue
        else:
            overlap_y = get_overlapping_segment(ari.y_seg, new_rectangle.y_seg)

        pending_rectangles = compute_pending_activation(new_rectangle, overlap_x, overlap_y)
        pending_area = sum([pr.area for pr in pending_rectangles])
        assert new_rectangle.area == SimpleRectangle(overlap_x, overlap_y).area + pending_area
        break

    if pending_rectangles is None:
        active_rectangles.append(new_rectangle)
    else:
        for pr in pending_rectangles:
            rectangle_activate(active_rectangles, pr)
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def rectangle_deactivate(active_rectangles: List[SimpleRectangle],
                         new_rectangle: SimpleRectangle) -> None:

    replace_index = None
    pending_rectangles = None
    for i in range(len(active_rectangles)):
        ari = active_rectangles[i]

        if not check_overlap(ari.x_seg, new_rectangle.x_seg):
            continue
        else:
            overlap_x = get_overlapping_segment(ari.x_seg, new_rectangle.x_seg)

        if not check_overlap(ari.y_seg, new_rectangle.y_seg):
            continue
        else:
            overlap_y = get_overlapping_segment(ari.y_seg, new_rectangle.y_seg)

        replace_index = i
        pending_rectangles = compute_remaining_active(ari, overlap_x, overlap_y)
        pending_area = sum([pr.area for pr in pending_rectangles])
        assert ari.area == SimpleRectangle(overlap_x, overlap_y).area + pending_area
        break

    if pending_rectangles is not None:
        del active_rectangles[replace_index]
        active_rectangles += pending_rectangles
        rectangle_deactivate(active_rectangles, new_rectangle)
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def calc_num_activated(cuboids: List[Cuboid], selected_indices: List[int]) -> int:

    selected_cuboids = []
    for i in selected_indices:
        selected_cuboids.append(cuboids[i])

    active_rectangles: List[SimpleRectangle]
    active_rectangles = []
    for i in range(len(selected_cuboids)):
        ci = selected_cuboids[i]
        rect = SimpleRectangle(ci.x_seg, ci.y_seg)
        if ci.action:
            rectangle_activate(active_rectangles, rect)
        else:
            rectangle_deactivate(active_rectangles, rect)

    total_area = 0
    for ar in active_rectangles:
        total_area += ar.area

    return total_area
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def compare_cuboid_lists(next_cuboid_list, prev_cuboid_list) -> bool:

    if len(next_cuboid_list) != len(prev_cuboid_list):
        return False

    for i in range(len(next_cuboid_list)):
        if next_cuboid_list[i] != prev_cuboid_list[i]:
            return False

    return True
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def main() -> None:

    with open('input.txt') as file:
        all_lines = [line for line in [line.strip() for line in file] if line]

    all_cuboids = []
    for next_line in all_lines:
        all_cuboids.append(Cuboid(next_line))

    result = part1(all_cuboids)
    print("sum(reactor) == %d" % result)

    cuboids_by_layer = {}
    for i in range(len(all_cuboids)):
        for z in all_cuboids[i].z_seg.range():
            if z not in cuboids_by_layer:
                cuboids_by_layer[z] = []
            cuboids_by_layer[z].append(i)

    unique_cuboids_table = []

    prev_cuboid_list = []
    for z in sorted(cuboids_by_layer.keys()):
        next_cuboid_list = cuboids_by_layer[z]
        if not compare_cuboid_lists(next_cuboid_list, prev_cuboid_list):
            unique_cuboids_table.append([next_cuboid_list, 1])
        else:
            unique_cuboids_table[-1][1] += 1

        prev_cuboid_list = next_cuboid_list

    total_activated = 0
    for i in range(len(unique_cuboids_table)):
        cuboid_list, num_layers = unique_cuboids_table[i]
        num_activated = calc_num_activated(all_cuboids, cuboid_list)
        num_activated *= num_layers
        total_activated += num_activated

    print("sum(reactor) == %d" % total_activated)
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    main()
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
# End of File
# ---------------------------------------------------------------------------------------------------------------------
