# ---------------------------------------------------------------------------------------------------------------------
# AoC 2021
# ---------------------------------------------------------------------------------------------------------------------
# 3.py
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
# More Imports
# ---------------------------------------------------------------------------------------------------------------------
from typing import List, Tuple


# ---------------------------------------------------------------------------------------------------------------------
def calc_rates(codes: List[str], index: int = 0, codes_ok: List[bool] = None) -> Tuple[int, int]:  # 0, 1

    rates = {"0": 0, "1": 0}

    for i in range(len(codes)):
        if codes_ok is None or codes_ok[i]:
            rates[codes[i][index]] += 1

    return rates["0"], rates["1"]
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def part1(codes: List[str]) -> Tuple[int, int]:  # gamma, epsilon

    gamma, epsilon = "", ""

    for i in range(len(codes[0])):

        r0, r1 = calc_rates(codes, i)

        if r0 > r1:
            gamma += "0"
            epsilon += "1"
        elif r1 > r0:
            epsilon += "0"
            gamma += "1"
        else:
            raise RuntimeError

    return int(gamma, 2), int(epsilon, 2)
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def part2(codes: List[str]) -> Tuple[int, int]:  # gamma, epsilon
    return part2_generator(codes), part2_scrubber(codes)
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def part2_generator(codes: List[str]) -> int:

    codes_ok = [True] * len(codes)
    bit_index = 0

    while sum(codes_ok) > 1:

        r0, r1 = calc_rates(codes, bit_index, codes_ok)

        for i in range(len(codes)):

            if not codes_ok[i]:
                continue

            if r0 <= r1:
                if codes[i][bit_index] == "0":
                    codes_ok[i] = False
            else:
                if codes[i][bit_index] == "1":
                    codes_ok[i] = False

        bit_index += 1

    for i in range(len(codes)):
        if codes_ok[i]:
            return int(codes[i], 2)

    raise RuntimeError
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def part2_scrubber(codes: List[str]) -> int:

    codes_ok = [True] * len(codes)
    bit_index = 0

    while sum(codes_ok) > 1:

        r0, r1 = calc_rates(codes, bit_index, codes_ok)

        for i in range(len(codes)):

            if not codes_ok[i]:
                continue

            if r0 <= r1:
                if codes[i][bit_index] == "1":
                    codes_ok[i] = False
            else:
                if codes[i][bit_index] == "0":
                    codes_ok[i] = False

        bit_index += 1

    for i in range(len(codes)):
        if codes_ok[i]:
            return int(codes[i], 2)

    raise RuntimeError
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def main() -> None:

    with open('input.txt') as f:
        f_lines = f.readlines()

    codes = []
    for fl in f_lines:
        codes.append(fl.strip())

    gamma, epsilon = part1(codes)
    print("gamma * epsilon = %d * %d = %d" %
          (gamma, epsilon, gamma * epsilon))

    generator, scrubber = part2(codes)
    print("generator * scrubber = %d * %d = %d" %
          (generator, scrubber, generator * scrubber))
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    main()
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
# End of File
# ---------------------------------------------------------------------------------------------------------------------
