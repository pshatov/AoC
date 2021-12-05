import matplotlib.pyplot as plt

from typing import List


def part12(depths: List[int], wnd_len=1) -> int:

    num_inc = 0
    for i in range(wnd_len, len(depths)):
        if depths[i] > depths[i-wnd_len]:
            num_inc += 1

    return num_inc


def graph(depths: List[int]):
    fig, ax = plt.subplots()

    ax.plot(range(len(depths)), [-d for d in depths])
    ax.set(xlabel='distance', ylabel='depth', title='Day 1')

    fig.savefig("depth.png")
    plt.show()


def main() -> None:

    with open('input.txt') as f:
        f_lines = f.readlines()

    depths = [int(fl.strip()) for fl in f_lines]

    num_inc1 = part12(depths)
    print(f"num_inc1 == {num_inc1}")

    num_inc2 = part12(depths, wnd_len=3)
    print(f"num_inc2 == {num_inc2}")

    # optional
    graph(depths)


if __name__ == '__main__':
    main()
