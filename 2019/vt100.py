import sys
import keyboard

def vt100_cursor_off():
    sys.stdout.write("\033[?25l")

def vt100_cursor_xy(x, y):
    sys.stdout.write("\033[%d;%dH" % (y+1, x+1))

def wait_key():
    done = False
    while not done:
        k = keyboard.read_event(suppress=True)
        if k.name == 'q' and k.event_type == "down": sys.exit()
        done = k.name == 'space' and k.event_type == "down"    
