import sys


SUBST = {'one':   1,
         'two':   2,
         'three': 3,
         'four':  4,
         'five':  5,
         'six':   6,
         'seven': 7,
         'eight': 8,
         'nine':  9}


def get_first_digit(line: str) -> int:
    for ch in line:
        if str.isdigit(ch):
            return int(ch)
    else:
        raise RuntimeError


def do_subst1(line: str) -> str:
    line_subst = ""
    while line:
        for digit in SUBST:
            if line.startswith(digit):
                line_subst += str(SUBST[digit])
                line = line[len(digit):]
                break
        else:
                line_subst += line[0]
                line = line[1:]

    return line_subst


def find_leftmost_digit(line: str) -> int:
    for n in range(len(line)):
        part = line[:n+1]
        if str.isdigit(part[-1]):
            return int(part[-1])
        for digit in SUBST:
            if part.endswith(digit):
                return SUBST[digit]
    
    raise RuntimeError


def find_rightmost_digit(line: str) -> int:
    for n in range(len(line)):
        part = line[-(n+1):]
        if str.isdigit(part[0]):
            return int(part[0])
        for digit in SUBST:
            if part.startswith(digit):
                return SUBST[digit]
    
    raise RuntimeError

    #         if line.startswith(digit):
    #             line_subst += SUBST[digit]
    #             line = line[len(digit):]
    #             break
    #     else:
    #             line_subst += line[0]
    #             line = line[1:]

    # return line_subst


def main() -> int:

    with open('day_01_full.txt') as f:
        all_lines = [l for l in [l.strip() for l in f] if l]

    sum1, sum2 = 0, 0
    for next_line in all_lines:

        #a1 = get_first_digit(next_line)
        #b1 = get_first_digit(reversed(next_line))
        #sum1 += 10 * a1 + b1

        next_line_subst = do_subst1(next_line)
        a2 = get_first_digit(next_line_subst)
        b2 = get_first_digit(reversed(next_line_subst))



        #a2 = find_leftmost_digit(next_line)
        #b2 = find_rightmost_digit(next_line)
        sum2 += 10 * a2 + b2
        print(f"{next_line} -> {a2}, {b2} = {sum2}")

    print(f"{sum1}")
    print(f"{sum2}")

    return 0


if __name__ == '__main__':
    sys.exit(main())
