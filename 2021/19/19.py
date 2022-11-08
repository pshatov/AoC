# ---------------------------------------------------------------------------------------------------------------------
# AoC 2021
# ---------------------------------------------------------------------------------------------------------------------
# 19.py
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------------------------------------------------
import numpy as np


# ---------------------------------------------------------------------------------------------------------------------
# More Imports
# ---------------------------------------------------------------------------------------------------------------------
from enum import Enum, IntEnum

from numpy import ndarray
from typing import List, Optional, Tuple


# ---------------------------------------------------------------------------------------------------------------------
class Axis(Enum):
    AxisX = 'X'
    AxisY = 'Y'
    AxisZ = 'Z'
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
class RotationAngle(IntEnum):
    Angle0 = 0
    Angle90 = 90
    Angle180 = 180
    Angle270 = 270
# ---------------------------------------------------------------------------------------------------------------------


SinLUT = {RotationAngle.Angle0: 0,
          RotationAngle.Angle90: 1,
          RotationAngle.Angle180: 0,
          RotationAngle.Angle270: -1}

CosLUT = {RotationAngle.Angle0: 1,
          RotationAngle.Angle90: 0,
          RotationAngle.Angle180: -1,
          RotationAngle.Angle270: 0}


RotationMatrices: List[ndarray]
RotationMatrices = []


# ---------------------------------------------------------------------------------------------------------------------
class Beacon:

    _xyz_relative: ndarray
    _xyz_absolute: Optional[ndarray]

    # -----------------------------------------------------------------------------------------------------------------
    def __init__(self, input_line: str) -> None:
        input_line_parts = input_line.split(',')
        assert len(input_line_parts) == len(Axis)
        self._xyz_relative = np.array([int(t) for t in input_line_parts], dtype=np.int_)
        self._xyz_absolute = None
    # -----------------------------------------------------------------------------------------------------------------

    # -----------------------------------------------------------------------------------------------------------------
    @property
    def xyz_relative(self) -> ndarray:
        return self._xyz_relative
    # -----------------------------------------------------------------------------------------------------------------

    # -----------------------------------------------------------------------------------------------------------------
    @property
    def xyz_absolute(self) -> ndarray:
        return self._xyz_absolute
    # -----------------------------------------------------------------------------------------------------------------

    # -----------------------------------------------------------------------------------------------------------------
    def map_absolute(self, xyz: ndarray) -> None:
        self._xyz_absolute = xyz
    # -----------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
class Sensor:

    beacons: List[Beacon]
    rotation_matrix: Optional[ndarray]
    shift: Optional[ndarray]
    number: int

    _beacons_xyz_absolute: Optional[ndarray]

    # -----------------------------------------------------------------------------------------------------------------
    def __init__(self, number: int) -> None:
        self.beacons = []
        self.rotation_matrix = None
        self.shift = None
        self.number = number

        self._beacons_xyz_absolute = None
        self._beacons_xyz_relative = None
    # -----------------------------------------------------------------------------------------------------------------

    # -----------------------------------------------------------------------------------------------------------------
    @property
    def beacons_xyz_absolute(self) -> ndarray:
        if self._beacons_xyz_absolute is None:
            self._beacons_xyz_absolute = list2ndarray([beacon.xyz_absolute for beacon in self.beacons])
        return self._beacons_xyz_absolute
    # -----------------------------------------------------------------------------------------------------------------

    # -----------------------------------------------------------------------------------------------------------------
    @property
    def beacons_xyz_relative(self) -> ndarray:
        if self._beacons_xyz_relative is None:
            self._beacons_xyz_relative = list2ndarray([beacon.xyz_relative for beacon in self.beacons])
        return self._beacons_xyz_relative
    # -----------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------


Sensors: List[Sensor]
Sensors = []


# ---------------------------------------------------------------------------------------------------------------------
def axis_rotation_matrix(axis: Axis, angle: RotationAngle) -> ndarray:
    if axis == Axis.AxisX:
        matrix = [[1, 0, 0],
                  [0, CosLUT[angle], -SinLUT[angle]],
                  [0, SinLUT[angle], CosLUT[angle]]]
    elif axis == Axis.AxisY:
        matrix = [[CosLUT[angle], 0, SinLUT[angle]],
                  [0, 1, 0],
                  [-SinLUT[angle], 0, CosLUT[angle]]]
    elif axis == Axis.AxisZ:
        matrix = [[CosLUT[angle], -SinLUT[angle], 0],
                  [SinLUT[angle], CosLUT[angle], 0],
                  [0, 0, 1]]
    else:
        raise RuntimeError
    return np.array(matrix, dtype=np.int_)
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def list2ndarray(src: List[ndarray]) -> ndarray:
    dst = None
    for t in src:
        if dst is None:
            dst = t
        else:
            dst = np.vstack((dst, t))
    return dst
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def np_dot_helper(matrix: ndarray, vector: ndarray) -> ndarray:
    return np.transpose(np.dot(matrix, np.transpose(vector)))
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def try_map_unknown_to_known(unknown_index: int, known_index: int) -> Optional[Tuple[ndarray, ndarray]]:

    known_points = Sensors[known_index].beacons_xyz_absolute
    unknown_points = Sensors[unknown_index].beacons_xyz_relative

    num_known_points = len(known_points)
    num_unknown_points = len(unknown_points)

    for rotation in RotationMatrices:

        unknown_points_rotated = np_dot_helper(rotation, unknown_points)

        next_shift_index = 0
        all_possible_shifts = np.zeros([num_known_points * num_unknown_points, len(Axis)])
        for source_index in range(num_known_points):
            for destination_index in range(num_unknown_points):

                next_shift = np.subtract(known_points[source_index], unknown_points_rotated[destination_index])
                all_possible_shifts[next_shift_index] = next_shift
                next_shift_index += 1

        unique_shifts, unique_shifts_counts = np.unique(all_possible_shifts, axis=0, return_counts=True)

        num_same_points = len(all_possible_shifts) - len(unique_shifts) + 1

        assert num_same_points <= 12

        if num_same_points == 12:
            target_shift = unique_shifts[unique_shifts_counts == 12][0]
            return rotation, target_shift

    return None
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def generate_rotation_matrices() -> None:
    for angle_x in RotationAngle:
        for angle_y in RotationAngle:
            for angle_z in RotationAngle:
                new_matrix = np.identity(len(Axis), dtype=np.int_)
                new_matrix = new_matrix.dot(axis_rotation_matrix(Axis.AxisX, angle_x))
                new_matrix = new_matrix.dot(axis_rotation_matrix(Axis.AxisY, angle_y))
                new_matrix = new_matrix.dot(axis_rotation_matrix(Axis.AxisZ, angle_z))
                for old_matrix in RotationMatrices:
                    if np.array_equal(new_matrix, old_matrix):
                        break
                else:
                    RotationMatrices.append(new_matrix)
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def map_all_beacons():

    pass_index = 0
    total_mapped = 0
    keep_mapping = True
    while keep_mapping:

        pass_index += 1
        print("Mapping beacons, pass: %d" % pass_index)

        num_mapped = 0
        for unknown_index in range(len(Sensors)):

            for known_index in range(len(Sensors)):

                if Sensors[known_index].rotation_matrix is None:
                    continue

                if Sensors[unknown_index].rotation_matrix is not None:
                    continue

                mapping_result = try_map_unknown_to_known(unknown_index, known_index)
                if mapping_result is None:
                    continue

                target_rotation, target_shift = mapping_result

                effective_target_rotation = target_rotation
                effective_target_shift = target_shift

                Sensors[unknown_index].rotation_matrix = effective_target_rotation
                Sensors[unknown_index].shift = effective_target_shift

                beacon_points = list2ndarray([beacon.xyz_relative for beacon in Sensors[unknown_index].beacons])
                beacon_points_rotated = np.transpose(np.dot(effective_target_rotation, np.transpose(beacon_points)))
                beacon_points_rotated_and_shifted = np.add(beacon_points_rotated, effective_target_shift)

                for i in range(len(beacon_points_rotated_and_shifted)):
                    Sensors[unknown_index].beacons[i].map_absolute(beacon_points_rotated_and_shifted[i])

                num_mapped += 1
                total_mapped += 1
                print("  > mapped sensor #%d against #%d (%d of %d)" %
                      (unknown_index, known_index, total_mapped, len(Sensors)))

        keep_mapping = num_mapped > 0
        if not keep_mapping:
            print("  > nothing left to map")
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def main() -> None:

    generate_rotation_matrices()

    with open('input.txt') as f:
        all_lines = [t.strip() for t in f.readlines()]
        all_lines = [t for t in all_lines if t]

    scanner_index = 0
    for next_line in all_lines:
        if "scanner" in next_line:
            Sensors.append(Sensor(scanner_index))
            scanner_index += 1
        else:
            Sensors[-1].beacons.append(Beacon(next_line))

    # hardcode rotation matrix and shift
    Sensors[0].rotation_matrix = RotationMatrices[0]
    Sensors[0].shift = np.array([0, 0, 0], dtype=np.int_)

    # assume origin is at sensor #0
    for i in range(len(Sensors[0].beacons)):
        Sensors[0].beacons[i].map_absolute(Sensors[0].beacons[i].xyz_relative)

    map_all_beacons()

    all_beacons = []
    for next_sensor in Sensors:
        all_beacons += next_sensor.beacons

    all_beacon_points = list2ndarray([beacon.xyz_absolute for beacon in all_beacons])
    unique_beacon_points = np.unique(all_beacon_points, axis=0)

    print("len(unique_beacon_points) == %d" % len(unique_beacon_points))

    distance_max = -1
    for i in range(len(Sensors)):
        for j in range(len(Sensors)):
            delta = np.subtract(Sensors[i].shift, Sensors[j].shift)
            distance = 0
            for k in range(len(Axis)):
                distance += int(np.abs(delta[k]))
            if distance > distance_max:
                distance_max = distance

    print("distance_max = %d" % distance_max)
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    main()
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
# End of File
# ---------------------------------------------------------------------------------------------------------------------
