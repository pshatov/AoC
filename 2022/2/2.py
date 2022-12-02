# ---------------------------------------------------------------------------------------------------------------------
# 2.py
# ---------------------------------------------------------------------------------------------------------------------
# AoC '22
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------------------------------------------------
from enum import Enum, auto
from typing import Tuple


# ---------------------------------------------------------------------------------------------------------------------
class RPS(Enum):
    Rock = auto()
    Paper = auto()
    Scissors = auto()
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
# Globals
# ---------------------------------------------------------------------------------------------------------------------
MoveLUT = {'A': RPS.Rock,
           'B': RPS.Paper,
           'C': RPS.Scissors,
           'X': RPS.Rock,
           'Y': RPS.Paper,
           'Z': RPS.Scissors}

ScoreLUT = {RPS.Rock:     1,
            RPS.Paper:    2,
            RPS.Scissors: 3}

RoundLUT = {(RPS.Rock,     RPS.Paper):    (0, 6),
            (RPS.Rock,     RPS.Scissors): (6, 0),
            (RPS.Paper,    RPS.Rock):     (6, 0),
            (RPS.Paper,    RPS.Scissors): (0, 6),
            (RPS.Scissors, RPS.Rock):     (0, 6),
            (RPS.Scissors, RPS.Paper):    (6, 0)}

DecryptLUT = {(RPS.Rock,     RPS.Rock):     RPS.Scissors,
              (RPS.Rock,     RPS.Scissors): RPS.Paper,
              (RPS.Paper,    RPS.Rock):     RPS.Rock,
              (RPS.Paper,    RPS.Scissors): RPS.Scissors,
              (RPS.Scissors, RPS.Rock):     RPS.Paper,
              (RPS.Scissors, RPS.Scissors): RPS.Rock}


# ---------------------------------------------------------------------------------------------------------------------
def play_round_part1(move0: RPS, move1: RPS) -> Tuple[int, int]:

    points0 = ScoreLUT[move0]
    points1 = ScoreLUT[move1]

    if move0 == move1:
        points0 += 3
        points1 += 3
    else:
        result0, result1 = RoundLUT[(move0, move1)]
        points0 += result0
        points1 += result1

    return points0, points1
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def play_round_part2(move0: RPS, move1_encrypted: RPS) -> Tuple[int, int]:
    move1 = decrypt_move(move0, move1_encrypted)
    return play_round_part1(move0, move1)
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def decrypt_move(move0: RPS, move1_encrypted: RPS) -> RPS:
    if move1_encrypted == RPS.Paper:
        return move0
    else:
        return DecryptLUT[(move0, move1_encrypted)]
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def main() -> None:

    with open('input.txt') as file:
        all_lines = [line for line in [line.strip() for line in file.readlines()] if line]

    score0, score1 = 0, 0
    for next_line in all_lines:
        symbol0, symbol1 = next_line.split(' ')
        move0, move1 = MoveLUT[symbol0], MoveLUT[symbol1]
        result0, result1 = play_round_part1(move0, move1)
        score0 += result0
        score1 += result1

    print("part 1: %d" % score1)

    score0, score1 = 0, 0
    for next_line in all_lines:
        symbol0, symbol1 = next_line.split(' ')
        move0, move1 = MoveLUT[symbol0], MoveLUT[symbol1]
        result0, result1 = play_round_part2(move0, move1)
        score0 += result0
        score1 += result1

    print("part 2: %d" % score1)
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    main()
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
# End of File
# ---------------------------------------------------------------------------------------------------------------------
