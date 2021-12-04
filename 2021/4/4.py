# ---------------------------------------------------------------------------------------------------------------------
# AoC 2021
# ---------------------------------------------------------------------------------------------------------------------
# 4.py
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
# More Imports
# ---------------------------------------------------------------------------------------------------------------------
from typing import List, Tuple


# ---------------------------------------------------------------------------------------------------------------------
class BoardClass:

    W = 5
    W1 = W + 1

    # -----------------------------------------------------------------------------------------------------------------
    def __init__(self, f_lines: List[str]) -> None:
        self.won = False
        self.lines = []
        for y in range(self.W):
            x = [int(xi) for xi in f_lines[y].strip().split(' ') if xi]
            self.lines.append(x)
    # -----------------------------------------------------------------------------------------------------------------

    # -----------------------------------------------------------------------------------------------------------------
    def mark(self, number: int) -> bool:

        if self.won:
            return False

        for y in range(self.W):
            for x in range(self.W):
                if self.lines[y][x] == number:
                    self.lines[y][x] = -1

        for y in range(self.W):
            if self._check_row(y):
                self.won = True
                return True

        for x in range(self.W):
            if self._check_col(x):
                self.won = True
                return True

        return False
    # -----------------------------------------------------------------------------------------------------------------

    # -----------------------------------------------------------------------------------------------------------------
    @property
    def sum(self):
        result = 0
        for y in range(self.W):
            for x in range(self.W):
                n = self.lines[y][x]
                if n > 0:
                    result += n
        return result
    # -----------------------------------------------------------------------------------------------------------------

    # -----------------------------------------------------------------------------------------------------------------
    def _check_row(self, y: int) -> bool:
        for x in range(self.W):
            if self.lines[y][x] >= 0:
                return False
        return True
    # -----------------------------------------------------------------------------------------------------------------

    # -----------------------------------------------------------------------------------------------------------------
    def _check_col(self, x: int) -> bool:
        for y in range(self.W):
            if self.lines[y][x] >= 0:
                return False
        return True
    # -----------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def part1(numbers, boards) -> Tuple[int, int]:  # unmarked_sum, last_index
    for i in range(len(numbers)):
        ni = numbers[i]
        for brd in boards:
            won = brd.mark(ni)
            if won:
                return brd.sum, i
    raise RuntimeError
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def part2(numbers, boards) -> Tuple[int, int]:  # unmarked_sum, last_index
    won_indices = []
    won_sums = []
    for i in range(len(numbers)):

        won_indices.append([])
        won_sums.append([])

        ni = numbers[i]
        for brd in boards:
            won = brd.mark(ni)
            if won:
                won_indices[-1].append(i)
                won_sums[-1].append(brd.sum)

    for i in range(len(numbers) - 1, -1, -1):
        if len(won_indices[i]) == 0:
            pass
        elif len(won_indices[i]) == 1:
            return won_sums[i][0], won_indices[i][0]
        else:
            raise RuntimeError

    raise RuntimeError
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def main() -> None:

    with open('input.txt') as f:
        f_lines = f.readlines()

    numbers = [int(x) for x in f_lines.pop(0).strip().split(',')]

    boards = []
    for i in range(len(f_lines) // 6):
        offset = BoardClass.W1 * i
        boards.append(BoardClass(f_lines[offset + 1: offset + BoardClass.W1]))

    unmarked_sum, last_index = part1(numbers, boards)
    last_number = numbers[last_index]
    print("unmarked_sum * last_number = %d * %d = %d" %
          (unmarked_sum, last_number, unmarked_sum * last_number))

    unmarked_sum, last_index = part2(numbers, boards)
    last_number = numbers[last_index]
    print("unmarked_sum * last_number = %d * %d = %d" %
          (unmarked_sum, last_number, unmarked_sum * last_number))
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    main()
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
# End of File
# ---------------------------------------------------------------------------------------------------------------------
