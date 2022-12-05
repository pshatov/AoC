# ---------------------------------------------------------------------------------------------------------------------
# 5.py
# ---------------------------------------------------------------------------------------------------------------------
# AoC '22
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------------------------------------------------
import re


# ---------------------------------------------------------------------------------------------------------------------
# More Imports
# ---------------------------------------------------------------------------------------------------------------------
from typing import List


# ---------------------------------------------------------------------------------------------------------------------
# Globals
# ---------------------------------------------------------------------------------------------------------------------
CmdRegExp = re.compile('^move (\\d+) from (\\d+) to (\\d+)$')


# ---------------------------------------------------------------------------------------------------------------------
def cmd_handler1(stacks: List[str], cmd_move: int, cmd_from: int, cmd_to: int) -> None:
    for i in range(cmd_move):
        stacks[cmd_to] += stacks[cmd_from][-1]
        stacks[cmd_from] = stacks[cmd_from][:-1]
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def cmd_handler2(stacks: List[str], cmd_move: int, cmd_from: int, cmd_to: int) -> None:
    stacks[cmd_to] += stacks[cmd_from][-cmd_move:]
    stacks[cmd_from] = stacks[cmd_from][:-cmd_move]
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def main() -> None:

    with open('input.txt') as file:
        all_lines = [line.rstrip() for line in file.readlines()]

    while not all_lines[-1]:
        all_lines = all_lines[:-1]

    crate_lines = []
    index_line = ""
    move_lines = []

    for next_line in all_lines:
        if not index_line:
            if next_line:
                crate_lines.append(next_line)
            else:
                index_line = crate_lines[-1]
                crate_lines = crate_lines[:-1]
        else:
            move_lines.append(next_line)

    index_line_parts = [int(t.strip()) for t in index_line.split(' ') if t]

    stacks = []
    num_stacks = len(index_line_parts)
    for i in range(num_stacks):
        assert index_line_parts[i] == i + 1
        stacks.append("")

    max_crate_line_len = max(len(t) for t in crate_lines)
    for i in range(len(crate_lines)):
        while len(crate_lines[i]) < max_crate_line_len:
            crate_lines[i] += " "

    stack_index = 0
    bottom_crate_line = crate_lines[-1]
    for ti in range(len(bottom_crate_line)):
        t = bottom_crate_line[ti]
        if str.isupper(t):
            assert bottom_crate_line[ti - 1] == '['
            assert bottom_crate_line[ti + 1] == ']'
            stacks[stack_index] += t
            for ji in range(len(crate_lines) - 2, -1, -1):
                j = crate_lines[ji][ti]
                if not str.isspace(j):
                    stacks[stack_index] += j
            stack_index += 1
    assert stack_index == num_stacks

    stacks_copy = stacks.copy()
    for cmd in move_lines:
        m = CmdRegExp.fullmatch(cmd)
        cmd_move, cmd_from, cmd_to = [int(t) - 1 for t in m.groups()]
        cmd_move += 1
        cmd_handler1(stacks_copy, cmd_move, cmd_from, cmd_to)

    msg = ""
    for t in stacks_copy:
        msg += t[-1]
    print("part 1: %s" % msg)

    stacks_copy = stacks.copy()
    for cmd in move_lines:
        m = CmdRegExp.fullmatch(cmd)
        cmd_move, cmd_from, cmd_to = [int(t) - 1 for t in m.groups()]
        cmd_move += 1
        cmd_handler2(stacks_copy, cmd_move, cmd_from, cmd_to)

    msg = ""
    for t in stacks_copy:
        msg += t[-1]
    print("part 2: %s" % msg)
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    main()
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
# End of File
# ---------------------------------------------------------------------------------------------------------------------
