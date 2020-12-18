LINES = []
with open('input.txt') as f:
    for fl in f:
        LINES.append('(' + fl.strip() + ')')

def extract_brackets(l):
    i_start = 0
    for i_stop in range(1, len(l)):
        if l[i_stop] == ')':
            a = '' if i_start == 0 else l[0:i_start]
            b = l[i_start+1:i_stop]
            c = '' if i_stop == len(l)-1 else l[i_stop+1:len(l)]
            return a, b, c
        elif l[i_stop] == '(':
            i_start = i_stop
    raise RuntimeError

def simplify_brackets1(b):
    bl = b.split(' ')
    r = int(bl[0])
    for bi in range(1, len(bl), 2):
        bx, by = bl[bi], int(bl[bi+1])
        if bx == '+': r += by
        elif bx == '*': r *= by
    return r

def simplify_brackets2(b):
    bl = b.split(' ')
    while '+' in bl:
        for bi in range(1, len(bl), 2):
            if bl[bi] == '+':
                bl[bi] = str(int(bl[bi-1]) + int(bl[bi+1]))
                del bl[bi+1]
                del bl[bi-1]
                break
    r = int(bl[0])
    for bi in range(2, len(bl), 2):
        r *= int(bl[bi])
    return r


def parse_line1(l):
    while l.startswith('('):
        a, b, c = extract_brackets(l)
        bb = simplify_brackets1(b)
        l = a + str(bb) + c
    return int(bb)

def parse_line2(l):
    while l.startswith('('):
        a, b, c = extract_brackets(l)
        bb = simplify_brackets2(b)
        l = a + str(bb) + c
    return int(bb)



s1 = 0
s2 = 0
for l in LINES:
    s1 += parse_line1(l)
    s2 += parse_line2(l)
print("s1: %d" % s1)
print("s2: %d" % s2)
