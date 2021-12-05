# ---------------------------------------------------------------------------------------------------------------------
# AoC 2021
# ---------------------------------------------------------------------------------------------------------------------
# 2.py
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------------------------------------------------
import matplotlib.pyplot as plt


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
def part1(commands: List[CommandClass], dp_list: List) -> int:

    depth, position = 0, 0

    dp_list.append((depth, position))
    for cmd in commands:
        if cmd.direction == DirectionEnum.Forward:
            position += cmd.distance
        elif cmd.direction == DirectionEnum.Down:
            depth += cmd.distance
        elif cmd.direction == DirectionEnum.Up:
            depth -= cmd.distance
        else:
            raise RuntimeError

        dp_list.append((depth, position))

    return depth * position
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def part2(commands: List[CommandClass], dp_list: List) -> int:

    depth, position, aim = 0, 0, 0

    dp_list.append((depth, position))
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

        dp_list.append((depth, position))

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

    dp1, dp2 = [], []

    r1 = part1(commands, dp1)
    print("r1 = %d" % r1)

    r2 = part2(commands, dp2)
    print("r2 = %d" % r2)

    graph(dp1, dp2)
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def graph(dp_list1: List, dp_list2: List):

    x1 = [dp[1] for dp in dp_list1]
    y1 = [-dp[0] for dp in dp_list1]

    x2 = [dp[1] for dp in dp_list2]
    y2 = [-dp[0] for dp in dp_list2]

    fig, axs = plt.subplots(1, 2)
    axs[0].plot(x1, y1)
    axs[1].plot(x2, y2)

    axs[0].set(xlabel='position', ylabel='depth', title="Part 1")
    axs[1].set(xlabel='position', ylabel='depth', title="Part 2")

    fig.tight_layout()
    fig.savefig('dp.png')

    plt.show()
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    main()
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
# End of File
# ---------------------------------------------------------------------------------------------------------------------
