import re

PROG = []
with open('input.txt') as f:
    for fl in f:
        fls = fl.strip()
        PROG.append(fls)

MEM = {}
MASK = None

p_re = re.compile("mem\[(\d+)\] = (\d+)")

def apply_mask(data):
    for mask_index in range(36):
        mask_char = MASK[35-mask_index]
        if mask_char == '0':
            data &= (0x3FFFFFFFFF ^ (1 << mask_index))
        elif mask_char == '1':
            data |= (1 << mask_index)
    return data
        

for p in PROG:
    if p.startswith('mask = '):
        MASK = p[-36:]
    else:
        m = p_re.fullmatch(p)
        if m is None: raise RuntimeError
        addr = int(m.group(1))
        data = int(m.group(2))
        data_mask = apply_mask(data)
        MEM[addr] = data_mask
    
sum = 0    
for d in MEM.values():
    if d > 0:
        sum += d
        
print("sum: %d" % sum)
        