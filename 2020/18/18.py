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

def simplify_brackets(b):
    bl = b.split(' ')
    r = int(bl[0])
    for bi in range(1, len(bl), 2):
        bx, by = bl[bi], int(bl[bi+1])
        if bx == '+': r += by
        elif bx == '*': r *= by
    return r

def parse_line(l):
    while l.startswith('('):
        a, b, c = extract_brackets(l)
        bb = simplify_brackets(b)
        l = a + str(bb) + c
    return int(bb)


s = 0
for l in LINES:
    s += parse_line(l)
print("s: %d" % s)
