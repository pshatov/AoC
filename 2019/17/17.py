import os
import sys
import keyboard

#from enum import IntEnum

sys.path.append(os.getcwd()+"\..")
from IntcodeClass import Intcode

field = []

cpu = Intcode()

def _vt100_cursor_off():
    print("\033[?25l", end='')
    
def _vt100_cursor_xy(x, y):
    print("\033[%d;%dH" % (y+1, x+1), end='')

def wait_key():
    done = False
    while not done:
        k = keyboard.read_event(suppress=True)
        if k.name == 'q' and k.event_type == "down": sys.exit()
        done = k.name == 'space' and k.event_type == "down"

def main():

    _vt100_cursor_off();

    opcodes = cpu.load_opcodes('input.txt')
    cpu.reset(opcodes)

    cpu.run()
    if not cpu.is_stopped: raise Exception("not cpu.is_stopped!")
    
    while cpu.can_pop_output():
        c = chr(cpu.pop_output( ))
        if c == "\n": field.append("")
        else:
            if len(field) == 0: field.append("")
            field[-1] += c
            
    field_temp = field.copy()
    field.clear()
    for ft in field_temp:
        if len(ft) > 0:
            field.append(ft.strip())
            
    _vt100_cursor_xy(0, 0)
    for i in range(len(field)):
        print("%s" % field[i])
    print("", flush=True)
            
    field_y = len(field)
    field_x = len(field[0])

    junctions = []
    for y in range(field_y):
        if y == 0: continue
        if y == (field_y-1): continue
        for x in range(field_x):
            if x == 0: continue
            if x == (field_x-1): continue
            if field[y-1][x  ] == "#" and \
               field[y+1][x  ] == "#" and \
               field[y  ][x-1] == "#" and \
               field[y  ][x+1] == "#" and \
               field[y  ][x  ] == "#":
                wait_key()
                xy = (x, y)
                junctions.append(xy)
                _vt100_cursor_xy(x, y)
                print("O", end='', flush=True)
            
        _vt100_cursor_xy(0, field_y)
        
    s = 0
    for j in junctions:
        jx, jy = j[0], j[1]
        s += jx * jy
        
    print("s = %d" % s)
        


if __name__ == "__main__":
    main()
