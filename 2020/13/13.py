with open('input.txt') as f:
    FL = f.readlines()

TS = int(FL[0])
BUS = []
for b in FL[1].strip().split(','):
    if b != 'x': BUS.append(int(b))
    
BUS_TS = {}
for b in BUS:
    if TS % b == 0: raise RuntimeError
    num_cyc = TS // b
    tx = b * (num_cyc + 1)
    BUS_TS[b] = tx

min_ts = BUS_TS[BUS[0]]
min_b = BUS[0]
for bi in range(1, len(BUS)):
    b = BUS[bi]
    bus_ts = BUS_TS[b]
    if bus_ts < min_ts:
        min_ts = bus_ts
        min_b = b

print("%d" % (min_b * (min_ts - TS)))
    
BUS_OFFSET = {}
offset = 0
for b in FL[1].strip().split(','):
    if b != 'x': BUS_OFFSET[int(b)] = offset
    offset += 1

print(BUS)

if BUS_OFFSET[BUS[0]] != 0: raise RuntimeError

t = 0
m = BUS[0]
for bi in range(1, len(BUS)):
    b = BUS[bi]
    b_o = BUS_OFFSET[b]
    while (t + b_o) % b != 0:
        t += m
    m *= b

print(t)
