ROUNDS = 200

NUM_CUPS = 20

LABELS = [9, 6, 3, 2, 7, 5, 4, 8, 1]
#LABELS = [3, 8, 9, 1, 2, 5, 4, 6, 7]


class Cups:

    def __init__(self, labels):
        self._labels = labels[:]
        while len(self._labels) < NUM_CUPS:
            self._labels.append(len(self._labels)+1)
        self._current_label = labels[0]

    @property
    def _current_index(self):
        return self._labels.index(self._current_label)

    def _print_cups(self):
        print("cups: ", end='')
        for i in range(NUM_CUPS):
            fmt = "(%3d)" if i == self._current_index else " %3d "
            print(fmt % self._labels[i], end='')
        #print()

    def round(self):

        self._print_cups()

        x = self._labels.pop((self._current_index + 1) % NUM_CUPS)
        y = self._labels.pop((self._current_index + 1) % (NUM_CUPS-1))
        z = self._labels.pop((self._current_index + 1) % (NUM_CUPS-2))

        #print("pick up: %d, %d, %d" % (x, y, z))

        destination_label = self._current_label - 1
        while True:
            if destination_label in [x, y, z]:
                destination_label = destination_label - 1
                continue
            if destination_label < min(self._labels):
                destination_label = max(self._labels)
                continue
            break

        #print("destination: %d" % destination_label)

        self._labels.insert(self._labels.index(destination_label)+1, z)
        self._labels.insert(self._labels.index(destination_label)+1, y)
        self._labels.insert(self._labels.index(destination_label)+1, x)

        self._current_label = self._labels[(self._current_index + 1) % NUM_CUPS]

        #print()

    def order(self):
        t = self._labels[:]
        while t[0] != 1:
            t0 = t.pop(0)
            t.append(t0)
        o = ""
        for i in range(1, NUM_CUPS):
            o += str(t[i])
        return o


def main():

    cups = Cups(LABELS)
    for r in range(ROUNDS):
        #print("-- move %d --" % (r+1), flush=True)
        cups.round()
        print ("-- %d" % (r+1))
    print(cups.order())


if __name__ == '__main__':
    main()
