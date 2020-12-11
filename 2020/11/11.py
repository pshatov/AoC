import copy

SEAT = []
NEW_SEAT = []


def load_seats():
    with open('input.txt') as f:
        for fl in f:
            fls = fl.strip()
            SEAT.append([])
            for flsc in fls:
                SEAT[-1].append(flsc)


def print_seats():
    for y in range(1, len(SEAT)-1):
        for x in range(1, len(SEAT[y])-1):
            print("%s" % SEAT[y][x], end='')
        print("")
    print("")

    
def patch_seats():
    for y in range(len(SEAT)):
        SEAT[y].insert(0, '.')
        SEAT[y].append('.')
    SEAT.insert(0, '.' * len(SEAT[0]))
    SEAT.append('.' * len(SEAT[-1]))
    for y in range(len(SEAT)):
        NEW_SEAT.append([])
        for x in range(len(SEAT[y])):
            NEW_SEAT[y].append(SEAT[y][x])


def calc_adj_seats1(x, y):
    tot = 0
    if SEAT[y-1][x-1] == '#': tot += 1
    if SEAT[y  ][x-1] == '#': tot += 1
    if SEAT[y+1][x-1] == '#': tot += 1
    if SEAT[y-1][x  ] == '#': tot += 1
    if SEAT[y+1][x  ] == '#': tot += 1
    if SEAT[y-1][x+1] == '#': tot += 1
    if SEAT[y  ][x+1] == '#': tot += 1
    if SEAT[y+1][x+1] == '#': tot += 1
    return tot


def calc_adj_seats2_dir(x0, y0, dx, dy):
    x = x0
    y = y0
    while True:
        x += dx
        y += dy
        if y == 0: return 0
        if x == 0: return 0
        if y == (len(SEAT)-1): return 0
        if x == (len(SEAT[y])-1): return 0
        if SEAT[y][x] == '#': return 1
        elif SEAT[y][x] == 'L': return 0


def calc_adj_seats2(x, y):
    tot = 0
    tot += calc_adj_seats2_dir(x, y, -1, -1)
    tot += calc_adj_seats2_dir(x, y,  0, -1)
    tot += calc_adj_seats2_dir(x, y, +1, -1)
    tot += calc_adj_seats2_dir(x, y, -1,  0)
    tot += calc_adj_seats2_dir(x, y, +1,  0)
    tot += calc_adj_seats2_dir(x, y, -1, +1)
    tot += calc_adj_seats2_dir(x, y,  0, +1)
    tot += calc_adj_seats2_dir(x, y, +1, +1)
    return tot
    

def mutate_seats1():
    chg = 0
    for y in range(1, len(SEAT)-1):
        for x in range(1, len(SEAT[y])-1):
            s = SEAT[y][x]
            s_new = s
            n = calc_adj_seats1(x, y)
            if s == 'L' and n == 0: s_new = '#'
            if s == '#' and n >= 4: s_new = 'L'
            NEW_SEAT[y][x] = s_new
    for y in range(1, len(SEAT)-1):
        for x in range(1, len(SEAT[y])-1):
            if NEW_SEAT[y][x] != SEAT[y][x]:
                chg += 1
            SEAT[y][x] = NEW_SEAT[y][x]
    return chg


def mutate_seats2():
    chg = 0
    for y in range(1, len(SEAT)-1):
        for x in range(1, len(SEAT[y])-1):
            s = SEAT[y][x]
            s_new = s
            n = calc_adj_seats2(x, y)
            if s == 'L' and n == 0: s_new = '#'
            if s == '#' and n >= 5: s_new = 'L'
            NEW_SEAT[y][x] = s_new
            
    for y in range(1, len(SEAT)-1):
        for x in range(1, len(SEAT[y])-1):
            if NEW_SEAT[y][x] != SEAT[y][x]:
                chg += 1
            SEAT[y][x] = NEW_SEAT[y][x]
    return chg
    
    
def main():
    load_seats()
    patch_seats()
    
    _S = copy.deepcopy(SEAT)
    
    while True:
        n = mutate_seats1()
        if n == 0:
            break

    tot = 0
    for y in range(1, len(SEAT)-1):
        for x in range(1, len(SEAT[y])-1):
            if SEAT[y][x] == '#': tot += 1
            SEAT[y][x] = _S[y][x] # !
    print("tot: %d" % tot)

    while True:
        n = mutate_seats2()
        if n == 0:
            break

    tot = 0
    for y in range(1, len(SEAT)-1):
        for x in range(1, len(SEAT[y])-1):
            if SEAT[y][x] == '#': tot += 1
    print("tot: %d" % tot)
    
    
if __name__ == '__main__':
    main()
            