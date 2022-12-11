# ---------------------------------------------------------------------------------------------------------------------
# 11.py
# ---------------------------------------------------------------------------------------------------------------------
# AoC '22
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------------------------------------------------
from typing import List


# ---------------------------------------------------------------------------------------------------------------------
# Settings
# ---------------------------------------------------------------------------------------------------------------------
DebugTurns = False
DebugRounds = True


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
    # -----------------------------------------------------------------------------------------------------------------

    # -----------------------------------------------------------------------------------------------------------------
    def __repr__(self) -> str:
        return "Monkey %d: [%s]" % (self.index, ', '.join([str(t) for t in self.items]))
    # -----------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def debug_turns(msg: str) -> None:
    if DebugTurns:
        print(msg)
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def debug_rounds(msg: str) -> None:
    if DebugRounds:
        print(msg)
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def play_round(all_monkeys: List[Monkey]) -> None:
    for monkey_index in range(len(all_monkeys)):
        m = all_monkeys[monkey_index]
        debug_turns("Monkey %d:" % monkey_index)
        while m.items:
            old = m.items[0]
            debug_turns("  Monkey inspects an item with a worry level of %d." % old)
            new = eval(m.operation)
            if '*' in m.operation:
                multiplier = m.operation.split(' ')[2]
                if multiplier == "old":
                    multiplier_str = "itself"
                elif str.isnumeric(multiplier):
                    multiplier_str = multiplier
                else:
                    raise RuntimeError
                debug_turns("    Worry level is multiplied by %s to %d." % (multiplier_str, new))
            elif '+' in m.operation:
                addend = eval(m.operation.split(' ')[2])
                debug_turns("    Worry level increases by %d to %d." % (addend, new))
            else:
                raise RuntimeError
            new //= 3
            debug_turns("    Monkey gets bored with item. Worry level is divided by 3 to %d." % new)

            if new % m.divisible > 0:
                debug_turns("    Current worry level is not divisible by %d." % m.divisible)
                all_monkeys[m.throw_if_false].items.append(new)
                debug_turns("    Item with worry level %d is thrown to monkey %d." % (new, m.throw_if_false))
            else:
                debug_turns("    Current worry level is divisible by %d." % m.divisible)
                all_monkeys[m.throw_if_true].items.append(new)
                debug_turns("    Item with worry level %d is thrown to monkey %d." % (new, m.throw_if_true))

            del m.items[0]
            m.business += 1
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

    for i in range(20):
        play_round(all_monkeys)
        debug_rounds("After round %d, the monkeys are holding items with these worry levels:" % (i + 1))
        for j in range(len(all_monkeys)):
            items_str = ', '.join([str(t) for t in all_monkeys[j].items])
            debug_rounds("Monkey %d: %s" % (j, items_str))
        debug_rounds('')

    businesses_sorted = sorted([m.business for m in all_monkeys], reverse=True)
    print("part 1: %d" % (businesses_sorted[0] * businesses_sorted[1]))
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    main()
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
# End of File
# ---------------------------------------------------------------------------------------------------------------------
