import os
import sys

sys.path.append(os.getcwd() + "\..")

from IntcodeClass import Intcode

XY0 = 15
Y1 = 50
Y2 = 2000
cpu = Intcode()
BEAM = []

def _vt100_cursor_off():
    print("\033[?25l", end='')
    
def _vt100_cursor_xy(x, y):
    print("\033[%d;%dH" % (y+1, x+1), end='')
    
def main():

    opcodes = Intcode.load_opcodes('input.txt')

    _vt100_cursor_off();
    _vt100_cursor_xy(0, 0);
    
    num_points = 0
    for y in range(XY0):
    
        s = ""
        for x in range(XY0):
            cpu.reset(opcodes)
            cpu.push_input(x)
            cpu.push_input(y)
            cpu.run()
            p = cpu.pop_output()
            if p == 0:
                s += "."
            elif p == 1:
                s += "#"
                num_points += 1
        
        print(s, flush=True)
        BEAM.append(s)

    xl = s.find("#")
    xr = s.rfind("#")

    for y in range(XY0, Y1):
        
        found = False
        while not found:
            cpu.reset(opcodes)
            cpu.push_input(xl)
            cpu.push_input(y)
            cpu.run()
            p = cpu.pop_output()
            if p == 0:
                xl += 1
            elif p == 1:
                found = True
                
        found = False
        while not found:
            cpu.reset(opcodes)
            cpu.push_input(xr)
            cpu.push_input(y)
            cpu.run()
            p = cpu.pop_output()
            if p == 1:
                xr += 1
            elif p == 0:
                xr -= 1
                found = True

        w = xr - xl + 1
        s = "." * xl + "#" * w
        num_points += w
            
        print(s, flush=True)
        BEAM.append(s)

    print("num_points = %d" % num_points)
        
    checking = False
    print("\nSkipping too narrow area...", flush=True)
    for y in range(Y1, Y2):
        
        found = False
        while not found:
            cpu.reset(opcodes)
            cpu.push_input(xl)
            cpu.push_input(y)
            cpu.run()
            p = cpu.pop_output()
            if p == 0:
                xl += 1
            elif p == 1:
                found = True
                
        found = False
        while not found:
            cpu.reset(opcodes)
            cpu.push_input(xr)
            cpu.push_input(y)
            cpu.run()
            p = cpu.pop_output()
            if p == 1:
                xr += 1
            elif p == 0:
                xr -= 1
                found = True

        w = xr - xl + 1
        s = "." * xl + "#" * w

        BEAM.append(s)
        
        if not checking:
            if y < 100: continue
            print("Narrow area skipped, searching for solution...\n", flush=True)
            checking = True
        
        y_dist = 0
        for yy in range(y, y-100, -1):
            b = BEAM[yy]
            if len(b) < (xl+1): break
            if b[xl] == "#":
                y_dist += 1
            else:
                break

        x_dist = len(BEAM[y-99]) - xl

        if (y % 100) == 0:
            print("Scanned %d y-lines..." % y)
            print("  beam x-offset: %d" % xl)
            print("  beam x-width: %d" % w)
            print("  fits y-size: %d " % y_dist)
            print("  fits x-size: %d " % x_dist)
            print("", end='', flush=True)

        if y_dist == 100 and x_dist == 100:
            print("SOLUTION FOUND!")
            print("%d" % (xl * 10000 + (y - 99)))
            break
    
if __name__ == "__main__":
    main()
