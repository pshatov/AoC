def load_passes(filename='input.txt'):
    r = []
    with open(filename) as f:
        for fl in f:
            r.append(fl.strip())
    return r

def _split_range(start, stop, dir):
    len_half = (stop - start + 1) // 2
    if dir > 0:
        return start + len_half, stop
    else:
        return start, stop - len_half

def decode_pass(p):
    rows = p[0:6+1]
    cols = p[7:9+1]

    r_start, r_stop = 0, 127
    for r in rows:
        r_dir = -1 if r == "F" else 1
        r_start, r_stop = _split_range(r_start, r_stop, r_dir)

    c_start, c_stop = 0, 7
    for c in cols:
        c_dir = -1 if c == "L" else 1
        c_start, c_stop = _split_range(c_start, c_stop, c_dir)

    return r_start, c_start







def main():

    PASSES = load_passes()
    
    id_max = -1
    for p in PASSES:
        p_row, p_col = decode_pass(p)
        id = (p_row << 3) + p_col
        if id > id_max: id_max = id
    
    print("id_max: %d" % id_max)






if __name__ == '__main__':
    main()
