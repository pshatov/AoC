import sys

from typing import List, Tuple


class Card:

    index: int
    winning_numbers: List[int]
    random_numbers: List[int]

    def __init__(self, line: str) -> None:
        card_part, numbers_part = [p.strip() for p in line.split(':')]
        assert card_part.startswith('Card ')
        self.index = int(card_part[5:])
        
        winning_part, random_part = [p.strip() for p in numbers_part.split('|')]

        self.winning_numbers = [int(p) for p in winning_part.split(' ') if p]
        self.random_numbers = [int(p) for p in random_part.split(' ') if p]

    @property
    def points(self) -> int:
        total = 0
        for n in self.winning_numbers:
            if n not in self.random_numbers:
                continue
            if total == 0:
                total = 1
            else:
                total *= 2
        return total
    
    @property
    def num_matches(self) -> int:
        total = 0
        for n in self.winning_numbers:
            if n in self.random_numbers:
                total += 1
        return total


def load_input(filename: str) -> List[Card]:

    with open(filename) as f:
        all_lines = [l for l in [l.strip() for l in f] if l]

    return [Card(l) for l in all_lines]


def part1(filename: str) -> Tuple[List[Card], int]:
    all_cards = load_input(filename)

    sum = 0
    for next_card in all_cards:
        sum += next_card.points

    return all_cards, sum


def part2(all_cards: List[Card]) -> int:

    card_counts = {}
    for offset, next_card in enumerate(all_cards):
        card_counts[offset] = 1

    for offset, next_card in enumerate(all_cards):
        assert next_card.index == offset + 1

        for i in range(1, next_card.num_matches + 1):
            if offset + i < len(all_cards):
                card_counts[offset + i] += card_counts[offset]

    return sum(card_counts.values())


def main() -> int:

    all_cards, sum1 = part1('day_04_input.txt')
    sum2 = part2(all_cards)

    print(f"{sum1}")
    print(f"{sum2}")

    return 0


if __name__ == '__main__':
    sys.exit(main())
