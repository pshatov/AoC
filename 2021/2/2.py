# ---------------------------------------------------------------------------------------------------------------------
# AoC 2021
# ---------------------------------------------------------------------------------------------------------------------
# 2.py
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
# More Imports
# ---------------------------------------------------------------------------------------------------------------------
from enum import Enum
from typing import List


# ---------------------------------------------------------------------------------------------------------------------
class DirectionEnum(Enum):
    Forward = 'forward'
    Down = 'down'
    Up = 'up'
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
class CommandClass:

    def __init__(self, direction: DirectionEnum, distance: int) -> None:
        self.direction = direction
        self.distance = distance
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def part1(commands: List[CommandClass]) -> int:

    depth, position = 0, 0

    for cmd in commands:
        if cmd.direction == DirectionEnum.Forward:
            position += cmd.distance
        elif cmd.direction == DirectionEnum.Down:
            depth += cmd.distance
        elif cmd.direction == DirectionEnum.Up:
            depth -= cmd.distance
        else:
            raise RuntimeError

    return depth * position
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def part2(commands: List[CommandClass]) -> int:

    depth, position, aim = 0, 0, 0

    for cmd in commands:
        if cmd.direction == DirectionEnum.Forward:
            position += cmd.distance
            depth += aim * cmd.distance
        elif cmd.direction == DirectionEnum.Down:
            aim += cmd.distance
        elif cmd.direction == DirectionEnum.Up:
            aim -= cmd.distance
        else:
            raise RuntimeError

    return depth * position
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def main() -> None:

    with open('input.txt') as f:
        f_lines = f.readlines()

    commands = []
    for fl in f_lines:
        fl_parts = fl.split(' ')
        cmd = CommandClass(DirectionEnum(fl_parts[0]), int(fl_parts[1].strip()))
        commands.append(cmd)

    r1 = part1(commands)
    print("r1 = %d" % r1)

    r2 = part2(commands)
    print("r2 = %d" % r2)
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    main()
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
# End of File
# ---------------------------------------------------------------------------------------------------------------------
