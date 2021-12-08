# ---------------------------------------------------------------------------------------------------------------------
# AoC 2021
# ---------------------------------------------------------------------------------------------------------------------
# 8.py
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
# More Imports
# ---------------------------------------------------------------------------------------------------------------------
from typing import List


# ---------------------------------------------------------------------------------------------------------------------
# Settings
# ---------------------------------------------------------------------------------------------------------------------
# noinspection SpellCheckingInspection
DIGIT_DICT = {'ABCEFG':  '0',
              'CF':      '1',
              'ACDEG':   '2',
              'ACDFG':   '3',
              'BCDF':    '4',
              'ABDFG':   '5',
              'ABDEFG':  '6',
              'ACF':     '7',
              'ABCDEFG': '8',
              'ABCDFG':  '9'}


# ---------------------------------------------------------------------------------------------------------------------
def decode(pattern: List[str], output: List[str]) -> int:

    for i in range(10):
        pattern[i] = ''.join(sorted(pattern[i]))

    for i in range(4):
        output[i] = ''.join(sorted(output[i]))

    p2, p3, p4, p7 = None, None, None, None
    p5, p6 = [], []
    for p in pattern:
        ps = set(p)
        pl = len(p)
        if pl == 2:
            p2 = ps
        elif pl == 3:
            p3 = ps
        elif pl == 4:
            p4 = ps
        elif pl == 7:
            p7 = ps
        elif pl == 5:
            p5.append(ps)
        elif pl == 6:
            p6.append(ps)
        else:
            raise RuntimeError

    #
    # 1 / 7 (2, 3)
    #
    z = set(p3) - set(p2)
    true_a, = z

    seg_dict = {true_a: 'A'}

    #
    # 2 / 5 / 3 (5)
    #
    h = set.intersection(*p5)

    z = set.intersection(p4, h)
    true_d, = z
    seg_dict[true_d] = 'D'

    z = h - {true_a, true_d}
    true_g, = z
    seg_dict[true_g] = 'G'

    z = p7 - p4 - {true_a, true_g}
    true_e, = z
    seg_dict[true_e] = 'E'

    z = p7 - p3 - {true_d, true_e, true_g}
    true_b, = z
    seg_dict[true_b] = 'B'

    for p in p5:
        if true_e in p:
            z = p - h - {true_e}
            true_c, = z
            seg_dict[true_c] = 'C'
        elif true_b in p:
            z = p - h - {true_b}
            true_f, = z
            seg_dict[true_f] = 'F'

    oo = ""
    for o in output:
        os = ""
        for oi in o:
            os += seg_dict[oi]
        oo += DIGIT_DICT[''.join(sorted(os))]

    return int(oo, 10)
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def main() -> None:

    with open('input.txt') as f:
        f_lines = [t.strip() for t in f.readlines()]

    patterns, outputs = [], []
    for fl in f_lines:
        pattern, output = fl.split(' | ')
        patterns.append(pattern.split(' '))
        outputs.append(output.split(' '))

    num1, num4, num7, num8 = 0, 0, 0, 0
    for o in outputs:
        for oi in o:
            if len(oi) == 2:
                num1 += 1
            elif len(oi) == 3:
                num7 += 1
            elif len(oi) == 4:
                num4 += 1
            elif len(oi) == 7:
                num8 += 1

    print("part 1: %d" % (num1 + num4 + num7 + num8))

    s = 0
    for i in range(len(outputs)):
        s += decode(patterns[i], outputs[i])

    print("part 2: %d" % s)
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    main()
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
# End of File
# ---------------------------------------------------------------------------------------------------------------------
