# ---------------------------------------------------------------------------------------------------------------------
# 18.py
# ---------------------------------------------------------------------------------------------------------------------
# AoC '22
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
# TODO: Rewrite using axes enum (or set?)!
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------------------------------------------------
import numpy as np


# ---------------------------------------------------------------------------------------------------------------------
# More Imports
# ---------------------------------------------------------------------------------------------------------------------
from typing import List


# ---------------------------------------------------------------------------------------------------------------------
class Side:

    # -----------------------------------------------------------------------------------------------------------------
    def __init__(self, x: float, y: float, z: float) -> None:
        self.active = True
        self.x, self.y, self.z = x, y, z
        if not isinstance(x, int):
            self.u, self.v, self.w = y, z, x
        elif not isinstance(y, int):
            self.u, self.v, self.w = x, z, y
        elif not isinstance(z, int):
            self.u, self.v, self.w = x, y, z
    # -----------------------------------------------------------------------------------------------------------------

    # -----------------------------------------------------------------------------------------------------------------
    def __eq__(self, other: 'Side') -> bool:
        return self.w == other.w and self.u == other.u and self.v == other.v
    # -----------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
class Cube:

    # -----------------------------------------------------------------------------------------------------------------
    def __init__(self, next_line: str) -> None:
        self.active = True
        self.x, self.y, self.z = [int(t) for t in next_line.split(',')]
    # -----------------------------------------------------------------------------------------------------------------

    # -----------------------------------------------------------------------------------------------------------------
    def __eq__(self, other: 'Cube') -> bool:
        return self.x == other.x and self.y == other.y and self.z == other.z
    # -----------------------------------------------------------------------------------------------------------------

    # -----------------------------------------------------------------------------------------------------------------
    def gen_sides_x(self) -> List[Side]:
        return [Side(self.x - 0.5, self.y, self.z), Side(self.x + 0.5, self.y, self.z)]
    # -----------------------------------------------------------------------------------------------------------------

    # -----------------------------------------------------------------------------------------------------------------
    def gen_sides_y(self) -> List[Side]:
        return [Side(self.x, self.y - 0.5, self.z), Side(self.x, self.y + 0.5, self.z)]
    # -----------------------------------------------------------------------------------------------------------------

    # -----------------------------------------------------------------------------------------------------------------
    def gen_sides_z(self) -> List[Side]:
        return [Side(self.x, self.y, self.z - 0.5), Side(self.x, self.y, self.z + 0.5)]
    # -----------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
class Space:

    # -----------------------------------------------------------------------------------------------------------------
    def __init__(self) -> None:
        self.x_min, self.x_max = 0, 0
        self.y_min, self.y_max = 0, 0
        self.z_min, self.z_max = 0, 0
    # -----------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
# Globals
# ---------------------------------------------------------------------------------------------------------------------
XYZ = Space()


# ---------------------------------------------------------------------------------------------------------------------
def mark_inactive_sides(all_sides: List[Side]) -> None:
    for i in range(len(all_sides)):
        for j in range(i + 1, len(all_sides)):
            if all_sides[i] == all_sides[j]:
                all_sides[i].active = False
                all_sides[j].active = False
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def count_active_sides(all_sides: List[Side]) -> int:
    result = 0
    for i in range(len(all_sides)):
        if all_sides[i].active:
            result += 1
    return result
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def mark_side_x(droplet_lava: np.ndarray, droplet_air: np.ndarray) -> None:
    for y in range(XYZ.y_min, XYZ.y_max + 1):
        for z in range(XYZ.z_min, XYZ.z_max + 1):
            if droplet_lava[XYZ.x_min, y, z] == 0:
                droplet_air[XYZ.x_min, y, z] = 1
            if droplet_lava[XYZ.x_max, y, z] == 0:
                droplet_air[XYZ.x_max, y, z] = 1
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def mark_side_y(droplet_lava: np.ndarray, droplet_air: np.ndarray) -> None:
    for x in range(XYZ.x_min, XYZ.x_max + 1):
        for z in range(XYZ.z_min, XYZ.z_max + 1):
            if droplet_lava[x, XYZ.y_min, z] == 0:
                droplet_air[x, XYZ.y_min, z] = 1
            if droplet_lava[x, XYZ.y_max, z] == 0:
                droplet_air[x, XYZ.y_max, z] = 1
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def mark_side_z(droplet_lava: np.ndarray, droplet_air: np.ndarray) -> None:
    for x in range(XYZ.x_min, XYZ.x_max + 1):
        for y in range(XYZ.y_min, XYZ.y_max + 1):
            if droplet_lava[x, y, XYZ.z_min] == 0:
                droplet_air[x, y, XYZ.z_min] = 1
            if droplet_lava[x, y, XYZ.z_max] == 0:
                droplet_air[x, y, XYZ.z_max] = 1
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def try_expand_x_left(droplet_lava: np.ndarray, droplet_air: np.ndarray, x: int, y: int, z: int) -> int:
    if x > XYZ.x_min and \
            droplet_lava[x - 1, y, z] == 0 and \
            droplet_air[x - 1, y, z] == 0:
        droplet_air[x - 1, y, z] = 1
        return 1
    return 0
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def try_expand_y_left(droplet_lava: np.ndarray, droplet_air: np.ndarray, x: int, y: int, z: int) -> int:
    if y > XYZ.y_min and \
            droplet_lava[x, y - 1, z] == 0 and \
            droplet_air[x, y - 1, z] == 0:
        droplet_air[x, y - 1, z] = 1
        return 1
    return 0
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def try_expand_z_left(droplet_lava: np.ndarray, droplet_air: np.ndarray, x: int, y: int, z: int) -> int:
    if z > XYZ.z_min and \
            droplet_lava[x, y, z - 1] == 0 and \
            droplet_air[x, y, z - 1] == 0:
        droplet_air[x, y, z - 1] = 1
        return 1
    return 0
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def try_expand_x_right(droplet_lava: np.ndarray, droplet_air: np.ndarray, x: int, y: int, z: int) -> int:
    if x < XYZ.x_max - 1 and \
            droplet_lava[x + 1, y, z] == 0 and \
            droplet_air[x + 1, y, z] == 0:
        droplet_air[x + 1, y, z] = 1
        return 1
    return 0
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def try_expand_y_right(droplet_lava: np.ndarray, droplet_air: np.ndarray, x: int, y: int, z: int) -> int:
    if y < XYZ.y_max - 1 and \
            droplet_lava[x, y + 1, z] == 0 and \
            droplet_air[x, y + 1, z] == 0:
        droplet_air[x, y + 1, z] = 1
        return 1
    return 0
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def try_expand_z_right(droplet_lava: np.ndarray, droplet_air: np.ndarray, x: int, y: int, z: int) -> int:
    if z < XYZ.z_max - 1 and \
            droplet_lava[x, y, z + 1] == 0 and \
            droplet_air[x, y, z + 1] == 0:
        droplet_air[x, y, z + 1] = 1
        return 1
    return 0
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def expand_in_x(droplet_lava: np.ndarray, droplet_air: np.ndarray, x: int) -> None:
    keep_expanding = True
    while keep_expanding:
        num_expanded = 0
        for y in range(XYZ.y_min, XYZ.y_max + 1):
            for z in range(XYZ.z_min, XYZ.z_max + 1):
                if droplet_air[x, y, z] == 1:
                    num_expanded += try_expand_y_left(droplet_lava, droplet_air, x, y, z)
                    num_expanded += try_expand_y_right(droplet_lava, droplet_air, x, y, z)
                    num_expanded += try_expand_z_left(droplet_lava, droplet_air, x, y, z)
                    num_expanded += try_expand_z_right(droplet_lava, droplet_air, x, y, z)

        keep_expanding = num_expanded > 0
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def expand_in_y(droplet_lava: np.ndarray, droplet_air: np.ndarray, y: int) -> None:
    keep_expanding = True
    while keep_expanding:
        num_expanded = 0
        for x in range(XYZ.x_min, XYZ.x_max + 1):
            for z in range(XYZ.z_min, XYZ.z_max + 1):
                if droplet_air[x, y, z] == 1:
                    num_expanded += try_expand_x_left(droplet_lava, droplet_air, x, y, z)
                    num_expanded += try_expand_x_right(droplet_lava, droplet_air, x, y, z)
                    num_expanded += try_expand_z_left(droplet_lava, droplet_air, x, y, z)
                    num_expanded += try_expand_z_right(droplet_lava, droplet_air, x, y, z)

        keep_expanding = num_expanded > 0
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def expand_in_z(droplet_lava: np.ndarray, droplet_air: np.ndarray, z: int) -> None:
    keep_expanding = True
    while keep_expanding:
        num_expanded = 0
        for x in range(XYZ.x_min, XYZ.x_max + 1):
            for y in range(XYZ.y_min, XYZ.y_max + 1):
                if droplet_air[x, y, z] == 1:
                    num_expanded += try_expand_x_left(droplet_lava, droplet_air, x, y, z)
                    num_expanded += try_expand_x_right(droplet_lava, droplet_air, x, y, z)
                    num_expanded += try_expand_y_left(droplet_lava, droplet_air, x, y, z)
                    num_expanded += try_expand_y_right(droplet_lava, droplet_air, x, y, z)

        keep_expanding = num_expanded > 0
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def walk_x_forward(droplet_lava: np.ndarray, droplet_air: np.ndarray) -> None:
    for x in range(XYZ.x_min + 1, XYZ.x_max):
        for y in range(XYZ.y_min, XYZ.y_max + 1):
            for z in range(XYZ.z_min, XYZ.z_max + 1):
                if droplet_lava[x, y, z] == 0 and droplet_air[x - 1, y, z] == 1:
                    droplet_air[x, y, z] = 1
        expand_in_x(droplet_lava, droplet_air, x)
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def walk_y_forward(droplet_lava: np.ndarray, droplet_air: np.ndarray) -> None:
    for y in range(XYZ.y_min + 1, XYZ.y_max):
        for x in range(XYZ.x_min, XYZ.x_max + 1):
            for z in range(XYZ.z_min, XYZ.z_max + 1):
                if droplet_lava[x, y, z] == 0 and droplet_air[x, y - 1, z] == 1:
                    droplet_air[x, y, z] = 1
        expand_in_y(droplet_lava, droplet_air, y)
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def walk_z_forward(droplet_lava: np.ndarray, droplet_air: np.ndarray) -> None:
    for z in range(XYZ.z_min + 1, XYZ.z_max):
        for x in range(XYZ.x_min, XYZ.x_max + 1):
            for y in range(XYZ.y_min, XYZ.y_max + 1):
                if droplet_lava[x, y, z] == 0 and droplet_air[x, y, z - 1] == 1:
                    droplet_air[x, y, z] = 1
        expand_in_z(droplet_lava, droplet_air, z)
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def walk_x_backward(droplet_lava: np.ndarray, droplet_air: np.ndarray) -> None:
    for x in range(XYZ.x_max - 1, XYZ.x_min, -1):
        for y in range(XYZ.y_min, XYZ.y_max + 1):
            for z in range(XYZ.z_min, XYZ.z_max + 1):
                if droplet_lava[x, y, z] == 0 and droplet_air[x + 1, y, z] == 1:
                    droplet_air[x, y, z] = 1
        expand_in_x(droplet_lava, droplet_air, x)
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def walk_y_backward(droplet_lava: np.ndarray, droplet_air: np.ndarray) -> None:
    for y in range(XYZ.y_max - 1, XYZ.y_min, -1):
        for x in range(XYZ.x_min, XYZ.x_max + 1):
            for z in range(XYZ.z_min, XYZ.z_max + 1):
                if droplet_lava[x, y, z] == 0 and droplet_air[x, y + 1, z] == 1:
                    droplet_air[x, y, z] = 1
        expand_in_y(droplet_lava, droplet_air, y)
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def walk_z_backward(droplet_lava: np.ndarray, droplet_air: np.ndarray) -> None:
    for z in range(XYZ.z_max - 1, XYZ.z_min, -1):
        for x in range(XYZ.x_min, XYZ.x_max + 1):
            for y in range(XYZ.y_min, XYZ.y_max + 1):
                if droplet_lava[x, y, z] == 0 and droplet_air[x, y, z + 1] == 1:
                    droplet_air[x, y, z] = 1
        expand_in_z(droplet_lava, droplet_air, z)
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def compute_surface_area(all_cubes: List[Cube]) -> int:

    all_sides_x: List[Side]
    all_sides_y: List[Side]
    all_sides_z: List[Side]

    all_sides_x = []
    all_sides_y = []
    all_sides_z = []
    for next_cube in all_cubes:
        all_sides_x += next_cube.gen_sides_x()
        all_sides_y += next_cube.gen_sides_y()
        all_sides_z += next_cube.gen_sides_z()

    mark_inactive_sides(all_sides_x)
    mark_inactive_sides(all_sides_y)
    mark_inactive_sides(all_sides_z)

    total_sides = 0
    total_sides += count_active_sides(all_sides_x)
    total_sides += count_active_sides(all_sides_y)
    total_sides += count_active_sides(all_sides_z)

    return total_sides
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def main() -> None:

    with open('input.txt') as file:
        all_lines = [line for line in [line.strip() for line in file] if line]

    all_cubes = []
    for next_line in all_lines:
        all_cubes.append(Cube(next_line))

    part1 = compute_surface_area(all_cubes)
    print("part 1: %d" % part1)

    XYZ.x_min, XYZ.x_max = all_cubes[0].x, all_cubes[0].x
    XYZ.y_min, XYZ.y_max = all_cubes[0].y, all_cubes[0].y
    XYZ.z_min, XYZ.z_max = all_cubes[0].z, all_cubes[0].z

    for i in range(1, len(all_cubes)):
        XYZ.x_min = min(XYZ.x_min, all_cubes[i].x)
        XYZ.y_min = min(XYZ.y_min, all_cubes[i].y)
        XYZ.z_min = min(XYZ.z_min, all_cubes[i].z)

    for i in range(1, len(all_cubes)):
        XYZ.x_max = max(XYZ.x_max, all_cubes[i].x)
        XYZ.y_max = max(XYZ.y_max, all_cubes[i].y)
        XYZ.z_max = max(XYZ.z_max, all_cubes[i].z)

    assert XYZ.x_min >= 0
    assert XYZ.y_min >= 0
    assert XYZ.z_min >= 0

    dx = XYZ.x_max - XYZ.x_min + 1
    dy = XYZ.y_max - XYZ.y_min + 1
    dz = XYZ.z_max - XYZ.z_min + 1

    droplet_shape = XYZ.x_max + 1, XYZ.y_max + 1, XYZ.z_max + 1
    droplet_lava = np.zeros(droplet_shape, dtype=np.int_)
    droplet_air = np.zeros(droplet_shape, dtype=np.int_)

    for next_cube in all_cubes:
        droplet_lava[next_cube.x, next_cube.y, next_cube.z] = 1

    mark_side_x(droplet_lava, droplet_air)
    mark_side_y(droplet_lava, droplet_air)
    mark_side_z(droplet_lava, droplet_air)

    walk_x_forward(droplet_lava, droplet_air)
    walk_x_backward(droplet_lava, droplet_air)

    walk_y_forward(droplet_lava, droplet_air)
    walk_y_backward(droplet_lava, droplet_air)

    walk_z_forward(droplet_lava, droplet_air)
    walk_z_backward(droplet_lava, droplet_air)

    all_bubbles = []
    for x in range(XYZ.x_min, XYZ.x_max + 1):
        for y in range(XYZ.y_min, XYZ.y_max + 1):
            for z in range(XYZ.z_min, XYZ.z_max + 1):
                if droplet_lava[x, y, z] == 0 and droplet_air[x, y, z] == 0:
                    all_bubbles.append(Cube("%d,%d,%d" % (x, y, z)))

    trapped_surface = compute_surface_area(all_bubbles)
    part2 = part1 - trapped_surface
    print("part 2: %d" % part2)
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    main()
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
# End of File
# ---------------------------------------------------------------------------------------------------------------------
