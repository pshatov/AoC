import os
import sys
import time

sys.path.append(os.getcwd() + "\\..\\..\\util")

from vt100 import vt100_cursor_off, vt100_cursor_xy

NR, NC = 128, 8

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

    r_start, r_stop = 0, NR-1
    for r in rows:
        r_dir = -1 if r == "F" else 1
        r_start, r_stop = _split_range(r_start, r_stop, r_dir)

    c_start, c_stop = 0, NC-1
    for c in cols:
        c_dir = -1 if c == "L" else 1
        c_start, c_stop = _split_range(c_start, c_stop, c_dir)

    return r_start, c_start

def encode_pass(r, c):
    return (r << 3) + c

def main():

    vt100_cursor_off()

    ROWS = []
    PASSES = load_passes()
    
    vt100_cursor_xy(0, 0)
    sys.stdout.write("pass_id_max = ?")

    for r in range(NR):
        ROWS.append([])
        for c in range(NC):
            ROWS[r].append(-1)
    
    for c in range(NC):
        vt100_cursor_xy(0, c+1)
        sys.stdout.write(NR * ".")
    sys.stdout.flush()
    
    id_max = -1
    for pn in range(len(PASSES)):
        
        p = PASSES[pn]
        p_row, p_col = decode_pass(p)
        id = encode_pass(p_row, p_col)
        if id > id_max: id_max = id
        
        ROWS[p_row][p_col] = id
        
        vt100_cursor_xy(0, 0)
        sys.stdout.write("pass_id_max = %d" % id_max)

        vt100_cursor_xy(p_row, p_col+1)
        sys.stdout.write("X")
        
        vt100_cursor_xy(0, 10)
        sys.stdout.write("pass_id = %4d (%3d)" % (id, pn+1))
        
        time.sleep(0.01)
        sys.stdout.flush()

    vt100_cursor_xy(0, 9)
    id_prev2, id_prev1 = -1, -1
    for r in range(NR):
        if r == 0:
            sys.stdout.write("<")
            continue
        elif r == (NR-1):
            sys.stdout.write(">")
            continue
        
        found = False
        for c in range(NC):
            id = ROWS[r][c]
        
            if id >= 0 and id_prev1 < 0 and id_prev2 >= 0:
                found = True
                my_id = id-1
        
            id_prev2, id_prev1 = id_prev1, id
        
        if found:
            vt100_cursor_xy(r-1, 9)
            sys.stdout.write("!")
        
        sys.stdout.write("-")
            
        time.sleep(0.05)
        sys.stdout.flush()

    vt100_cursor_xy(0, 11)
    sys.stdout.write("pass_id_my = %d" % my_id)

if __name__ == '__main__':
    main()
