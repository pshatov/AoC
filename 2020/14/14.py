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
    
def apply_mask_v2(addr):
    src_addr = []
    for bit_index in range(36):
        src_addr.append((addr & (1 << bit_index)) >> bit_index)
        
    for bit_index in range(36):
        mask_char = MASK[35-bit_index]
        if mask_char == '1':
            src_addr[bit_index] = 1
        elif mask_char == 'X':
            src_addr[bit_index] = -1
    
    dst_addr_list = [src_addr]
    for bit_index in range(36):
        if src_addr[bit_index] < 0:
            dst_addr_list_len = len(dst_addr_list)
            for j in range(dst_addr_list_len):
                dst_addr_list[j][bit_index] = 0
                dst_addr_list.append(list(dst_addr_list[j]))
                dst_addr_list[-1][bit_index] = 1

    dst_addr = []
    for j in range(len(dst_addr_list)):
        dst_addr.append(0)
        for bit_index in range(36):
            dst_addr[-1] |= (dst_addr_list[j][bit_index] << bit_index)
        

    #print(format(addr, "036b"))
    #print(MASK)
    #for i in range(len(dst_addr_list)):
        #for j in range(36):
            #print("%d" % dst_addr_list[i][35-j], end='')
        #print()
        
    #raise RuntimeError
        
        #if mask_char == '0':
            #data &= (0x3FFFFFFFFF ^ (1 << mask_index))
        #elif mask_char == '1':
            #data |= (1 << mask_index)
    #return data
    
    return dst_addr
        

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



MEM.clear()

for p in PROG:
    if p.startswith('mask = '):
        MASK = p[-36:]
    else:
        m = p_re.fullmatch(p)
        if m is None: raise RuntimeError
        addr = int(m.group(1))
        data = int(m.group(2))
        addr_mask = apply_mask_v2(addr)
        for a in addr_mask:
            MEM[a] = data

sum = 0    
for d in MEM.values():
    if d > 0:
        sum += d
        
print("sum: %d" % sum)
