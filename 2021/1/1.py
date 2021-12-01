from typing import List


def part1(depths: List[int]) -> int:

    num_inc = 0
    for i in range(1, len(depths)):
        if depths[i] > depths[i-1]:
            num_inc += 1

    return num_inc


def part2(depths: List[int], wnd_len=3) -> int:

    num_inc = 0
    for i in range(wnd_len, len(depths)):
        if depths[i] > depths[i-wnd_len]:
            num_inc += 1

    return num_inc


def main() -> None:

    with open('input.txt') as f:
        f_lines = f.readlines()

    depths = [int(fl.strip()) for fl in f_lines]

    num_inc1 = part1(depths)
    print(f"num_inc1 == {num_inc1}")

    num_inc2 = part2(depths)
    print(f"num_inc2 == {num_inc2}")


if __name__ == '__main__':
    main()
