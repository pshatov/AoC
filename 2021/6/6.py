# ---------------------------------------------------------------------------------------------------------------------
# AoC 2021
# ---------------------------------------------------------------------------------------------------------------------
# 6.py
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------------------------------------------------
import matplotlib.pyplot as plt


# ---------------------------------------------------------------------------------------------------------------------
# More Imports
# ---------------------------------------------------------------------------------------------------------------------
from typing import Dict, List


# ---------------------------------------------------------------------------------------------------------------------
def step(fish: Dict[int, int]) -> None:

    fish_new = {}

    for i in range(9):
        fish_new[i] = 0

    for i in range(1, 9):
        fish_new[i - 1] = fish[i]
    fish_new[8] += fish[0]
    fish_new[6] += fish[0]

    for i in range(9):
        fish[i] = fish_new[i]
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def main() -> None:

    with open('input.txt') as f:
        f_line = f.readline()

    fish = {}
    for i in range(9):
        fish[i] = 0

    for f in f_line.strip().split(','):
        fish[int(f)] += 1

    n1 = []
    for i in range(80):
        step(fish)
        n1.append(sum(fish.values()))

    print("part 1: %d" % n1[-1])

    n2 = n1[:]
    for i in range(256 - 80):
        step(fish)
        n2.append(sum(fish.values()))

    print("part 2: %d" % n2[-1])

    graph(n1, n2)
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def graph(n1: List[int], n2: List[int]):

    fig, axs = plt.subplots(1, 2)
    axs[0].plot(range(len(n1)), n1)
    axs[1].plot(range(len(n2)), n2)

    axs[0].set(xlabel='day', ylabel='population', title="Part 1")
    axs[1].set(xlabel='day', ylabel='population', title="Part 2")

    fig.tight_layout()
    fig.savefig('population.png')

    plt.show()
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    main()
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
# End of File
# ---------------------------------------------------------------------------------------------------------------------
