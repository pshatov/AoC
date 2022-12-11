# ---------------------------------------------------------------------------------------------------------------------
# 11.py
# ---------------------------------------------------------------------------------------------------------------------
# AoC '22
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------------------------------------------------
from copy import deepcopy
from typing import Tuple, List, Optional


# ---------------------------------------------------------------------------------------------------------------------
class Monkey:

    _MarkerStartingItems = 'Starting items: '
    _MarkerOperation = 'Operation: new = '
    _MarkerDivisible = 'Test: divisible by '
    _MarkerIfTrue = 'If true: throw to monkey '
    _MarkerIfFalse = 'If false: throw to monkey '

    # -----------------------------------------------------------------------------------------------------------------
    def __init__(self, index: int, lines: List[str]):

        assert len(lines) == 6

        # Monkey 0:
        line_monkey = lines[0]
        assert line_monkey.endswith(':')
        line_monkey = line_monkey[:-1]
        line_monkey_parts = line_monkey.split(' ')
        assert len(line_monkey_parts) == 2
        assert line_monkey_parts[0] == 'Monkey'
        assert int(line_monkey_parts[1]) == index
        self.index = index

        # Starting items: 79, 98
        line_items = lines[1]
        assert line_items.startswith(Monkey._MarkerStartingItems)
        line_items = line_items[len(Monkey._MarkerStartingItems):].replace(' ', '')
        self.items = [int(t) for t in line_items.split(',')]

        # Operation: new = old * 19
        line_operation = lines[2]
        assert line_operation.startswith(Monkey._MarkerOperation)
        line_operation = line_operation[len(Monkey._MarkerOperation):]
        self.operation = line_operation

        # Test: divisible by 23
        line_divisible = lines[3]
        assert line_divisible.startswith(Monkey._MarkerDivisible)
        line_divisible = line_divisible[len(Monkey._MarkerDivisible):]
        self.divisible = int(line_divisible)

        # If true: throw to monkey 2
        # If false: throw to monkey 3
        line_true = lines[4]
        line_false = lines[5]
        assert line_true.startswith(Monkey._MarkerIfTrue)
        assert line_false.startswith(Monkey._MarkerIfFalse)
        line_true = line_true[len(Monkey._MarkerIfTrue):]
        line_false = line_false[len(Monkey._MarkerIfFalse):]
        self.throw_if_true = int(line_true)
        self.throw_if_false = int(line_false)

        self.business = 0
        self.modulo = None
    # -----------------------------------------------------------------------------------------------------------------

    # -----------------------------------------------------------------------------------------------------------------
    def __repr__(self) -> str:
        return "Monkey %d: [%s]" % (self.index, ', '.join([str(t) for t in self.items]))
    # -----------------------------------------------------------------------------------------------------------------

    # -----------------------------------------------------------------------------------------------------------------
    def inspect(self, limit: bool) -> Optional[Tuple[int, int]]:
        old = self.items[0]
        new = eval(self.operation)

        if limit:
            new //= 3
        else:
            assert self.modulo is not None
            new %= self.modulo

        if new % self.divisible > 0:
            next_monkey = self.throw_if_false
        else:
            next_monkey = self.throw_if_true

        del self.items[0]
        self.business += 1

        return next_monkey, new
    # -----------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def play_round(all_monkeys: List[Monkey], limit: Optional[bool] = True) -> None:
    for monkey_index in range(len(all_monkeys)):
        m = all_monkeys[monkey_index]
        while m.items:
            next_monkey, new = m.inspect(limit)
            all_monkeys[next_monkey].items.append(new)
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def main() -> None:

    with open('input.txt') as file:
        all_lines = [line for line in [line.strip() for line in file] if line]

    assert len(all_lines) % 6 == 0

    all_monkeys = []
    num_monkeys = len(all_lines) // 6
    for i in range(num_monkeys):
        all_monkeys.append(Monkey(i, all_lines[6 * i: 6 * (i + 1)]))

    monkeys1 = deepcopy(all_monkeys)
    for i in range(20):
        play_round(monkeys1)

    businesses_sorted = sorted([m.business for m in monkeys1], reverse=True)
    print("part 1: %d" % (businesses_sorted[0] * businesses_sorted[1]))

    monkeys2 = deepcopy(all_monkeys)
    modulo = 1
    for m in monkeys2:
        modulo *= m.divisible
    for m in monkeys2:
        m.modulo = modulo

    for i in range(10000):
        play_round(monkeys2, limit=False)

    businesses_sorted = sorted([m.business for m in monkeys2], reverse=True)
    print("part 2: %d" % (businesses_sorted[0] * businesses_sorted[1]))
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    main()
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
# End of File
# ---------------------------------------------------------------------------------------------------------------------
