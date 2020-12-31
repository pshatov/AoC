import sys

# LABELS = [3, 8, 9, 1, 2, 5, 4, 6, 7]    # example
LABELS = [9, 6, 3, 2, 7, 5, 4, 8, 1]   # input

NUM_CUPS = 9
ROUNDS = 10

CUPS = []


class LinkedCup:

    def __init__(self, label, left, right):

        self.label = label
        self.left = left
        self.right = right


def create_initial_cups():
    for i in range(len(LABELS)):
        CUPS.append(LinkedCup(LABELS[i], None, None))


def create_remaining_cups():
    i = len(CUPS)
    while len(CUPS) < NUM_CUPS:
        i += 1
        CUPS.append(LinkedCup(i, None, None))


def create_cup_links():
    for i in range(1, len(CUPS)-1):
        CUPS[i].left = CUPS[i-1]
        CUPS[i].right = CUPS[i+1]
    CUPS[0].left = CUPS[-1]
    CUPS[0].right = CUPS[1]
    CUPS[-1].left = CUPS[-2]
    CUPS[-1].right = CUPS[0]


def shuffle_cups_round(destination_cup, silent=True):

    pick_x = destination_cup.right
    pick_y = pick_x.right
    pick_z = pick_y.right

    pick_labels = [pick_x.label, pick_y.label, pick_z.label]

    if not silent:
        print("pick up: %d, %d, %d" % tuple(pick_labels))

    new_destination_label = destination_cup.label - 1

    while True:
        if new_destination_label in pick_labels:
            new_destination_label -= 1
            continue
        if new_destination_label < 1:
            new_destination_label = len(CUPS)
            continue
        break

    potential_left = destination_cup.left
    potential_right = destination_cup.right
    while True:
        if potential_left.label == new_destination_label:
            new_destination_cup = potential_left
            break
        if potential_right.label == new_destination_label:
            new_destination_cup = potential_right
            break
        potential_left = potential_left.left
        potential_right = potential_right.right

    if not silent:
        print("destination: %d" % new_destination_cup.label)
        print()

    destination_cup.right = pick_z.right
    t = new_destination_cup.right
    new_destination_cup.right = pick_x
    pick_z.right = t

    return destination_cup.right


def print_cups(destination_cup):
    print("cups: ", end='')
    t = destination_cup
    for r in range(len(CUPS)):
        fmt = " %d " if r > 0 else "(%d)"
        print(fmt % t.label, end='')
        t = t.right
    print()


def solve_part1():
    r = ""
    c = None
    for i in range(len(CUPS)):
        if CUPS[i].label == 1:
            c = CUPS[i]
            break
    for i in range(len(CUPS)-1):
        c = c.right
        r += str(c.label)
    print(r)


def solve_part2():
    c = None
    for i in range(len(CUPS)):
        if CUPS[i].label == 1:
            c = CUPS[i]
            break
    x = c.right.label
    y = c.right.right.label
    z = x * y
    print(str(x))
    print(str(y))
    print(str(z))


def main():

    global NUM_CUPS
    global ROUNDS

    create_initial_cups()
    create_cup_links()
    destination_cup = CUPS[0]
    for r in range(ROUNDS):
        print("-- move %d --" % (r+1))
        print_cups(destination_cup)
        destination_cup = shuffle_cups_round(destination_cup, silent=False)

    solve_part1()

    # patch parameters
    NUM_CUPS = 1000 * 1000
    ROUNDS = 10 * 1000 * 1000

    CUPS.clear()
    create_initial_cups()
    create_remaining_cups()
    create_cup_links()
    destination_cup = CUPS[0]
    for r in range(ROUNDS):
        if (r % 100000) == 99999:
            print("-- move %d --" % (r + 1))
            sys.stdout.flush()
        destination_cup = shuffle_cups_round(destination_cup)

    solve_part2()


if __name__ == '__main__':
    main()
