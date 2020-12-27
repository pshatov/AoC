ROUNDS = 100

LABELS = [9, 6, 3, 2, 7, 5, 4, 8, 1]
#LABELS = [3, 8, 9, 1, 2, 5, 4, 6, 7]


class Cups:

    def __init__(self, labels):
        self._labels = labels[:]
        self._current_label = labels[0]

    @property
    def _current_index(self):
        return self._labels.index(self._current_label)

    def _print_cups(self):
        print("cups: ", end='')
        for i in range(9):
            fmt = "(%d)" if i == self._current_index else " %d "
            print(fmt % self._labels[i], end='')
        print()

    def round(self):

        self._print_cups()

        x = self._labels.pop((self._current_index + 1) % 9)
        y = self._labels.pop((self._current_index + 1) % 8)
        z = self._labels.pop((self._current_index + 1) % 7)

        print("pick up: %d, %d, %d" % (x, y, z))

        destination_label = self._current_label - 1
        while True:
            if destination_label in [x, y, z]:
                destination_label = destination_label - 1
                continue
            if destination_label < min(self._labels):
                destination_label = max(self._labels)
                continue
            break

        print("destination: %d" % destination_label)

        self._labels.insert(self._labels.index(destination_label)+1, z)
        self._labels.insert(self._labels.index(destination_label)+1, y)
        self._labels.insert(self._labels.index(destination_label)+1, x)

        self._current_label = self._labels[(self._current_index + 1) % 9]

        print()

    def order(self):
        t = self._labels[:]
        while t[0] != 1:
            t0 = t.pop(0)
            t.append(t0)
        o = ""
        for i in range(1, 9):
            o += str(t[i])
        return o


    #
    #The crab places the cups it just picked up so that they are immediately clockwise of the destination cup. They keep the same order as when they were picked up.
    #The crab selects a new current cup: the cup which is immediately clockwise of the current cup.

    


def main():

    cups = Cups(LABELS)
    for r in range(ROUNDS):
        print("-- move %d --" % (r+1))
        cups.round()
    print(cups.order())


if __name__ == '__main__':
    main()
