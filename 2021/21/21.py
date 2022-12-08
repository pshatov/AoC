# ---------------------------------------------------------------------------------------------------------------------
# AoC 2021
# ---------------------------------------------------------------------------------------------------------------------
# 21.py
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------------------------------------------------
from copy import deepcopy
from typing import Tuple, Dict


# ---------------------------------------------------------------------------------------------------------------------
# Globals
# ---------------------------------------------------------------------------------------------------------------------
AllPossibleStates = []


# ---------------------------------------------------------------------------------------------------------------------
class DeterministicDice:

    # -----------------------------------------------------------------------------------------------------------------
    def __init__(self):
        self._num_rolls = 0
        self._value = 0
    # -----------------------------------------------------------------------------------------------------------------

    # -----------------------------------------------------------------------------------------------------------------
    def roll(self) -> int:

        self._num_rolls += 1

        t = self._value

        self._value += 1
        self._value %= 100

        return t + 1
    # -----------------------------------------------------------------------------------------------------------------

    # -----------------------------------------------------------------------------------------------------------------
    @property
    def num_rolls(self) -> int:
        return self._num_rolls
    # -----------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
class UniverseState:

    # -----------------------------------------------------------------------------------------------------------------
    def __init__(self):
        self.matrix = {}
        for p_state in AllPossibleStates:
            self.matrix[p_state] = {}
            for other_p_state in AllPossibleStates:
                self.matrix[p_state][other_p_state] = 0
    # -----------------------------------------------------------------------------------------------------------------

    # -----------------------------------------------------------------------------------------------------------------
    @staticmethod
    def state_encode(position: int, score: int) -> int:
        return position * 100 + score
    # -----------------------------------------------------------------------------------------------------------------

    # -----------------------------------------------------------------------------------------------------------------
    @staticmethod
    def state_decode(state: int) -> Tuple[int, int]:
        score = state % 100
        position = (state - score) // 100
        return position, score
    # -----------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def move1(p: int, s: int, d: DeterministicDice) -> Tuple[int, int]:

    a = d.roll()
    b = d.roll()
    c = d.roll()
    d = a + b + c

    p += d
    p %= 10

    s += (p + 1)

    return p, s
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def move2(position: int, roll: int) -> Tuple[int, int]:
    next_position = (position + roll) % 10
    extra_score = next_position + 1
    return next_position, extra_score
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def play_round2(p_universe: UniverseState, other_p_universe: UniverseState,
                all_possible_rolls_lut: Dict[int, int]) -> Tuple[UniverseState, UniverseState, int]:

    won = 0
    p_universe_new = deepcopy(p_universe)
    other_p_universe_new = deepcopy(other_p_universe)

    for p_state in AllPossibleStates:
        for other_p_state in AllPossibleStates:

            old_count = p_universe.matrix[p_state][other_p_state]
            if old_count == 0:
                continue

            old_position, old_score = UniverseState.state_decode(p_state)
            p_universe_new.matrix[p_state][other_p_state] -= old_count
            other_p_universe_new.matrix[other_p_state][p_state] -= old_count

            for roll in all_possible_rolls_lut:
                new_count = old_count * all_possible_rolls_lut[roll]
                new_position, extra_score = move2(old_position, roll)
                new_score = old_score + extra_score
                new_state = UniverseState.state_encode(new_position, new_score)
                if new_score > 20:
                    won += new_count
                else:
                    p_universe_new.matrix[new_state][other_p_state] += new_count
                    other_p_universe_new.matrix[other_p_state][new_state] += new_count

    return p_universe_new, other_p_universe_new, won
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def main() -> None:

    with open('input.txt') as f:
        fl1, fl2 = [t.strip() for t in f.readlines()]

    p1 = int(fl1.split(':')[1]) - 1
    p2 = int(fl2.split(':')[1]) - 1

    initial_position_p1, initial_position_p2 = p1, p2

    dd = DeterministicDice()

    s1, s2 = 0, 0
    while True:
        p1, s1 = move1(p1, s1, dd)
        if s1 >= 1000:
            z = s2 * dd.num_rolls
            break
        p2, s2 = move1(p2, s2, dd)
        if s2 >= 1000:
            z = s1 * dd.num_rolls
            break

    print("part 1: %d" % z)

    all_possible_rolls_lut = {}
    for a in range(1, 4):
        for b in range(1, 4):
            for c in range(1, 4):
                d = a + b + c
                if d not in all_possible_rolls_lut:
                    all_possible_rolls_lut[d] = 0
                all_possible_rolls_lut[d] += 1

    for position in range(10):
        for score in range(21):
            state = UniverseState.state_encode(position, score)
            AllPossibleStates.append(state)

    universe_p1 = UniverseState()
    universe_p2 = UniverseState()

    state_p1 = UniverseState.state_encode(initial_position_p1, 0)
    state_p2 = UniverseState.state_encode(initial_position_p2, 0)

    universe_p1.matrix[state_p1][state_p2] = 1
    universe_p2.matrix[state_p2][state_p1] = 1

    round_count = 0
    keep_playing = 20
    won_p1, won_p2 = 0, 0
    while keep_playing > 0:
        round_count += 1

        if round_count % 2 == 1:
            universe_p1, universe_p2, won = play_round2(universe_p1, universe_p2, all_possible_rolls_lut)
            won_p1 += won
        else:
            universe_p2, universe_p1, won = play_round2(universe_p2, universe_p1, all_possible_rolls_lut)
            won_p2 += won

        keep_playing -= 1

    print("part 2: %d" % max(won_p1, won_p2))
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    main()
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
# End of File
# ---------------------------------------------------------------------------------------------------------------------
