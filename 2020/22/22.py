P1 = []
P2 = []

f_lines = []
with open('input.txt') as f:
    for l in f:
        f_lines.append(l.strip())

if f_lines[0] != 'Player 1:': raise RuntimeError
del f_lines[0]
while f_lines[0]:
    P1.append(f_lines[0])
    del f_lines[0]
del f_lines[0]
if f_lines[0] != 'Player 2:': raise RuntimeError
del f_lines[0]
P2 = f_lines[:]

play = True
while play:
    p1 = int(P1[0])
    p2 = int(P2[0])

    del P1[0]
    del P2[0]

    if p1 == p2: raise RuntimeError
    elif p1 > p2:
        P1.append(p1)
        P1.append(p2)
    else:
        P2.append(p2)
        P2.append(p1)

    if len(P1) == 0 or len(P2) == 0: play = False

P = P1 if len(P2) == 0 else P2

score = 0
for i in range(1, len(P)+1):
    score += P[-i] * i

print("score: %d" % score)


