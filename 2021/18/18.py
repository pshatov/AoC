# ---------------------------------------------------------------------------------------------------------------------
# AoC 2021
# ---------------------------------------------------------------------------------------------------------------------
# 18.py
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
# More Imports
# ---------------------------------------------------------------------------------------------------------------------
from enum import Enum, auto
from typing import Union, Pattern


# ---------------------------------------------------------------------------------------------------------------------
class PartType(Enum):
    Literal = auto()
    Pair = auto()
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
class PartPosition(Enum):
    Left = auto()
    Root = auto()
    Right = auto()
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
class PairPart:

    type: PartType
    value_literal: int
    value_pair: 'Pair'

    # -----------------------------------------------------------------------------------------------------------------
    def __init__(self, value: Union[int, 'Pair']) -> None:

        if isinstance(value, int):
            self.type = PartType.Literal
            self.value_literal = value
        else:
            self.type = PartType.Pair
            self.value_pair = value
    # -----------------------------------------------------------------------------------------------------------------

    # -----------------------------------------------------------------------------------------------------------------
    def format(self) -> str:
        if self.type == PartType.Literal:
            return "%d" % self.value_literal
        else:
            return self.value_pair.format()
    # -----------------------------------------------------------------------------------------------------------------

    # -----------------------------------------------------------------------------------------------------------------
    def __repr__(self) -> str:
        return "%d" % self.value_literal if self.type == PartType.Literal else str(self.value_pair)
    # -----------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
class Pair:

    x: PairPart
    y: PairPart
    parent: 'Pair'
    level: int
    position_parent: PartPosition
    cant_explode: bool

    # -----------------------------------------------------------------------------------------------------------------
    def __init__(self, parent: 'Pair' = None, level: int = 1,
                 position_parent: PartPosition = PartPosition.Root) -> None:
        self.parent = parent
        self.level = level
        self.position_parent = position_parent
        self.cant_explode = False
    # -----------------------------------------------------------------------------------------------------------------

    # -----------------------------------------------------------------------------------------------------------------
    def set_xy(self, x: Union[int, 'Pair'], y: Union[int, 'Pair']) -> None:
        self.x = PairPart(x)
        self.y = PairPart(y)
    # -----------------------------------------------------------------------------------------------------------------

    # -----------------------------------------------------------------------------------------------------------------
    def format(self) -> str:
        return "[%s,%s]" % (self.x.format(), self.y.format())
    # -----------------------------------------------------------------------------------------------------------------

    # -----------------------------------------------------------------------------------------------------------------
    def __repr__(self) -> str:
        return "[%s,%s]" % (str(self.x), str(self.y))
    # -----------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def parse_number(s: str, parent: Pair = None, level: int = 1, position: PartPosition = PartPosition.Root) -> Pair:

    if not s.startswith('['):
        raise RuntimeError

    p = Pair(parent, level, position)
    x, y = -1, -1
    comma_seen = False
    part_x, part_y = "", ""
    num_opened, num_closed = 0, 0
    num_opened_x, num_closed_x = 0, 0
    num_opened_y, num_closed_y = 0, 0

    i = 0
    while i < len(s):
        c = s[i]

        if c == '[':
            num_opened += 1
            if not comma_seen:
                num_opened_x += 1
            else:
                num_opened_y += 1

        elif c == ']':
            num_closed += 1
            if not comma_seen:
                num_closed_x += 1
            else:
                num_closed_y += 1

        elif c == ',':
            if num_opened - num_closed == 1:
                comma_seen = True

        elif c.isdigit():
            pass

        else:
            raise RuntimeError

        if not comma_seen:
            part_x += c
        else:
            part_y += c

        if c == ',' and num_opened - num_closed == 1:
            if num_opened_x > 1:
                x = parse_number(part_x[1:], p, level + 1, PartPosition.Left)
            else:
                x = int(part_x[1:])

        if c == ']' and num_closed == num_opened:
            if num_opened_y > 0:
                y = parse_number(part_y[1:-1], p, level + 1, PartPosition.Right)
            else:
                y = int(part_y[1:-1])

            if (i + 1) != len(s):
                raise RuntimeError

        i += 1

    p.set_xy(x, y)

    return p
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def add(x: Pair, y: Pair) -> Pair:

    if x.parent is not None or y.parent is not None:
        raise RuntimeError

    z = Pair()
    z.set_xy(x, y)

    return z
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def reset_cant_explode(p: Pair) -> None:

    p.cant_explode = False

    if p.x.type == PartType.Pair:
        reset_cant_explode(p.x.value_pair)

    if p.y.type == PartType.Pair:
        reset_cant_explode(p.y.value_pair)
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def reduce_explode_helper_simple(p: Pair, v: int, pos: PartPosition) -> bool:

    if pos == PartPosition.Left and p.x.type == PartType.Literal:
        p.x.value_literal += v
        return True

    if pos == PartPosition.Right and p.y.type == PartType.Literal:
        p.y.value_literal += v
        return True

    return False
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def reduce_explode_helper_right(p: Pair, v: int, pos: PartPosition) -> bool:

    if reduce_explode_helper_simple(p, v, pos):
        return True

    # right part? -> can only go up
    if pos == PartPosition.Right:
        return reduce_explode_helper_right(p.parent, v, p.position_parent)

    # left part -> try to scan
    else:
        if reduce_explode_helper_right(p.x.value_pair, v, PartPosition.Left):
            return True
        else:
            return reduce_explode_helper_right(p.y.value_pair, v, PartPosition.Right)
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def reduce_explode_helper_left(p: Pair, v: int, pos: PartPosition) -> bool:

    #if pos == PartPosition.Left and p.x.type == PartType.Literal:
        #p.x.value_literal += v

    #else:
        pass


# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def reduce_explode(p: Pair, result: int = 0) -> int:

    assert p is not None

    if result > 0:
        return result

    if p.level < 5:
        if p.x.type == PartType.Pair:
            result += reduce_explode(p.x.value_pair, result)
        if p.y.type == PartType.Pair:
            result += reduce_explode(p.y.value_pair, result)

    elif p.level == 5:

        assert p.x.type == PartType.Literal
        assert p.y.type == PartType.Literal

        reduce_explode_helper_left(p.parent, p.x.value_literal, p.position_parent)
        reduce_explode_helper_right(p.parent, p.y.value_literal, p.position_parent)

        if p.position_parent == PartPosition.Root:
            raise RuntimeError
        elif p.position_parent == PartPosition.Left:
            p.parent.x = PairPart(0)
        elif p.position_parent == PartPosition.Right:
            p.parent.y = PairPart(0)

        result += 1

    else:
        raise RuntimeError

    return result
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def reduce_split(p: Pair) -> int:
    pass
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def reduce(p: Pair) -> None:
    repeat = True
    while repeat:
        reset_cant_explode(p)
        x = reduce_explode(p)
        y = reduce_split(p)
        repeat = x > 0 or y > 0
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def main() -> None:

    with open('input.txt') as f:
        f_lines = [t.strip() for t in f.readlines()]

    numbers = []
    for fl in f_lines:
        n = parse_number(fl)
        numbers.append(n)

    zs = "[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]"
    print(zs)

    z = parse_number(zs)
    print(z.format())

    print()

    reduce_explode(z)
    print("[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]")
    print(z.format())

    return

    s = None
    for n in numbers:
        if s is None:
            s = n
        else:
            s = add(s, n)
            reduce(s)

    print()
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    main()
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
# End of File
# ---------------------------------------------------------------------------------------------------------------------
