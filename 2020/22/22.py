P1 = []
P2 = []
game_cnt = 0


def load_input():
    P1.clear()
    P2.clear()

    f_lines = []
    with open('input.txt') as f:
        for fl in f:
            f_lines.append(fl.strip())

    if f_lines[0] != 'Player 1:': raise RuntimeError
    del f_lines[0]
    while f_lines[0]:
        P1.append(int(f_lines[0]))
        del f_lines[0]
    del f_lines[0]
    if f_lines[0] != 'Player 2:': raise RuntimeError
    del f_lines[0]
    while len(f_lines) > 0:
        P2.append(int(f_lines[0]))
        del f_lines[0]


def play_simple():
    play = True
    while play:
        p1 = P1.pop(0)
        p2 = P2.pop(0)

        if p1 == p2: raise RuntimeError
        elif p1 > p2:
            P1.append(p1)
            P1.append(p2)
        else:
            P2.append(p2)
            P2.append(p1)

        if len(P1) == 0 or len(P2) == 0: play = False


def calc_score():
    p = P1 if len(P2) == 0 else P2

    score = 0
    for i in range(1, len(p)+1):
        score += p[-i] * i

    return score


def play_recursive(p1, p2):

    global game_cnt

    game_cnt += 1
    my_cnt = game_cnt

    #if my_cnt > 1: print()
    #print("=== Game %d ===" % my_cnt)

    states_p1 = []
    states_p2 = []

    rnd = 1
    while True:

        #print()
        #print("-- Round %d (Game %d) --" % (rnd, my_cnt))

        #print("Player 1's deck: ", end='')
        #for i in range(len(p1)):
        #    if i > 0: print(", ", end='')
        #    print("%d" % p1[i], end='')
        #print()
        #print("Player 2's deck: ", end='')
        #for i in range(len(p2)):
        #    if i > 0: print(", ", end='')
        #    print("%d" % p2[i], end='')
        #print()

        if p1 in states_p1 and p2 in states_p2:
            p2.clear()
            return True
        else:
            states_p1.append(p1[:])
            states_p2.append(p2[:])

        p1v = p1.pop(0)
        p2v = p2.pop(0)

        #print("Player 1 plays: %d" % p1v)
        #print("Player 2 plays: %d" % p2v)

        if len(p1) >= p1v and len(p2) >= p2v:
            p1c = p1[:p1v]
            p2c = p2[:p2v]
            #print("Playing a sub - game to determine the winner...")
            w = play_recursive(p1c, p2c)
            #print()
            #print("...anyway, back to game %d." % my_cnt)
        else:
            w = p1v > p2v

        #if w:
        #    print("Player 1 wins round %d of game %d!" % (rnd, my_cnt))
        #else:
        #    print("Player 2 wins round %d of game %d!" % (rnd, my_cnt))

        if w:
            p1.append(p1v)
            p1.append(p2v)
        else:
            p2.append(p2v)
            p2.append(p1v)

        if len(p2) == 0:
        #    print("The winner of game %d is player 1!" % my_cnt)
            return True

        if len(p1) == 0:
        #    print("The winner of game %d is player 2!" % my_cnt)
            return False

        rnd += 1


def main():

    load_input()
    play_simple()
    score = calc_score()
    print("score: %d" % score)

    load_input()
    play_recursive(P1, P2)
    score = calc_score()
    print("score: %d" % score)


if __name__ == '__main__':
    main()
