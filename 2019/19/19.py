import os
import sys
#import keyboard

sys.path.append(os.getcwd()+"\..")
from IntcodeClass import Intcode

XY = 50
cpu = Intcode()

def _vt100_cursor_off():
    print("\033[?25l", end='')
    
def _vt100_cursor_xy(x, y):
    print("\033[%d;%dH" % (y+1, x+1), end='')
    
def main():

    opcodes = cpu.load_opcodes('input.txt')

    _vt100_cursor_off();
    _vt100_cursor_xy(0, 0);
    
    num_points = 0
    for y in range(XY):
    
        for x in range(XY):
            cpu.reset(opcodes)
            cpu.push_input(x)
            cpu.push_input(y)
            cpu.run()
            p = cpu.pop_output()
            if   p == 0:
                print(".", end='')
            elif p == 1:
                print("#", end='')
                num_points += 1
        print("", flush=True)
        
    print("num_points = %d" % num_points)

    
    
    
if __name__ == "__main__":
    main()
