import sys

from enum import IntEnum
from typing import List, Tuple, Optional, Dict


class Strength(IntEnum):
    FiveOfKind = 6
    FourOfKind = 5
    FullHouse = 4
    ThreeOfKind = 3
    TwoPair = 2
    OnePair = 1
    HighCard = 0


POWER_LUT = "AKQJT98765432"


class Hand:

    cards: str
    bid: int
    _strength: Optional[int]
    _power_lut: str

    def __init__(self, cards: str, bid: int, power_lut: str) -> None:
        self.cards = cards
        self.bid = bid
        self._strength = None
        self._power_lut = power_lut

    @property
    def strength(self) -> int:
        assert self._strength is not None
        return self._strength
    
    def update_power_lut(self, power_lut: str) -> None:
        self._power_lut = power_lut
    
    def calc_strength(self) -> None:
                
        card_counts = self._card_counts()

        counts = ''.join([str(c) for c in sorted(card_counts.values(), reverse=True)])
        if counts == "5":
            self._strength = Strength.FiveOfKind
        elif counts == "41":
            self._strength = Strength.FourOfKind
        elif counts == "32":
            self._strength = Strength.FullHouse
        elif counts == "311":
            self._strength = Strength.ThreeOfKind
        elif counts == "221":
            self._strength = Strength.TwoPair
        elif counts == "2111":
            self._strength = Strength.OnePair
        elif counts == "11111":
            self._strength = Strength.HighCard
        else:
            raise RuntimeError

    def calc_strength_joker(self) -> None:
                
        card_counts = self._card_counts()

        counts = ''.join([str(c) for c in sorted(card_counts.values(), reverse=True)])
        
        if counts == "5":
            self._strength = Strength.FiveOfKind
        
        elif counts == "41":
            if "J" in card_counts:
                self._strength = Strength.FiveOfKind
            else:
                self._strength = Strength.FourOfKind
        
        elif counts == "32":
            if "J" in card_counts:
                self._strength = Strength.FiveOfKind
            else:
                self._strength = Strength.FullHouse
        
        elif counts == "311":
            if "J" in card_counts:
                self._strength = Strength.FourOfKind
            else:
                self._strength = Strength.ThreeOfKind
        
        elif counts == "221":
            if "J" in card_counts:
                if card_counts["J"] == 2:
                    self._strength = Strength.FourOfKind
                else:
                    self._strength = Strength.FullHouse
            else:
                self._strength = Strength.TwoPair
        
        elif counts == "2111":
            if "J" in card_counts:
                self._strength = Strength.ThreeOfKind
            else:
                self._strength = Strength.OnePair
        
        elif counts == "11111":
            if "J" in card_counts:
                assert card_counts["J"] == 1
                self._strength = Strength.OnePair
            else:
                self._strength = Strength.HighCard
        
        else:
            raise RuntimeError

    def __lt__(self, other: 'Hand') -> bool:

        if self.strength != other.strength:
            return self.strength < other.strength
        
        for i in range(len(self.cards)):
            power_self = self._power_lut.find(self.cards[i])
            power_other = self._power_lut.find(other.cards[i])
            if power_self != power_other:
                return power_self > power_other
        
        raise RuntimeError
    
    def _card_counts(self) -> Dict:
        card_counts = {}
        for next_card in self.cards:
            if next_card not in card_counts:
                card_counts[next_card] = 0
            card_counts[next_card] += 1
        return card_counts


def load_input(filename: str) -> List[Hand]:

    with open(filename) as f:
        all_lines = [l for l in [l.strip() for l in f] if l]

    all_hands = []
    for next_line in all_lines:
        hand, bid = tuple(next_line.split(' '))
        assert len(hand) == 5
        all_hands.append(Hand(hand, int(bid), POWER_LUT))

    return all_hands


def part1(filename: str) -> Tuple[List[Hand], int]:    
    all_hands = load_input(filename)
    for next_hand in all_hands:
        next_hand.calc_strength()
    return all_hands, calc_total(all_hands)


def calc_total(hands: List[Hand]) -> int:
    answer = 0
    for index, next_hand in enumerate(sorted(hands)):
        answer += next_hand.bid * (index + 1)
    return answer


def part2(all_hands: List[Hand]) -> int:
    POWER_LUT_JOKER = POWER_LUT.replace('J', '') + 'J'
    for next_hand in all_hands:
        next_hand.calc_strength_joker()
        next_hand.update_power_lut(POWER_LUT_JOKER)
    return calc_total(all_hands)


def main() -> int:

    all_hands, answer1 = part1('day_07_input.txt')
    answer2 = part2(all_hands)

    print(f"{answer1}")
    print(f"{answer2}")

    return 0


if __name__ == '__main__':
    sys.exit(main())
