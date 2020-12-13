import os
import sys

sys.path.append(os.getcwd() + "\\..")
from IntcodeClass import Intcode


cpu = Intcode()


def _vt100_cursor_off():
    print("\033[?25l", end='')
    
def _vt100_cursor_xy(x, y):
    print("\033[%d;%dH" % (y+1, x+1), end='')
    
def send_instr(s):
    for i in range(len(s)):
        cpu.push_input(ord(s[i]))
    cpu.push_input(ord("\n"))
    
def main():

    opcodes = Intcode.load_opcodes('input.txt')

    _vt100_cursor_off();
    _vt100_cursor_xy(0, 0);
    
    cpu.reset(opcodes)
    
    #   A B C D
    # | . . . . | ?
    # | . . . X | JUMP
    # | . . X . |
    # | . . X X | JUMP
    # | . X . . |
    # | . X . X | JUMP
    # | . X X . |
    # | . X X X | JUMP
    # | X . . . |
    # | X . . X | JUMP
    # | X . X . |
    # | X . X X | JUMP
    # | X X . . |
    # | X X . X | JUMP
    # | X X X . |
    # | X X X X |
    
    # | . . . X | JUMP
    # | . . X X | JUMP
    # | . X . X | JUMP
    # | . X X X | JUMP
    # | X . . X | JUMP
    # | X . X X | JUMP
    # | X X . X | JUMP
    
    #
    # We must jump when D has ground and at least one tile in A..C has a hole:
    # J = D AND (NOT ((A AND B) AND C))
    #
    
    instr = ["NOT A J", # J = NOT A
             "NOT J T", # T = NOT J = NOT (NOT A) = A
             "AND B T", # T = B AND T = A AND B
             "AND C T", # T = C AND T = (A AND B) AND C
             "NOT T J", # J = NOT T = NOT ((A AND B) AND C)
             "AND D J", # J = D AND J = D AND (NOT ((A AND B) AND C))
             "WALK"]
             
    for i in instr:
        if len(i) > 0:
            send_instr(i)
            
    cpu.run()
    
    while cpu.can_pop_output():
        p = cpu.pop_output()
        if p < 128:
            print(chr(p), end='')
        else:
            print("Result: %d" % p)
            break
    
    
    
if __name__ == "__main__":
    main()
