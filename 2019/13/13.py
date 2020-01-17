import os
import sys
import time
import keyboard
sys.path.append(os.getcwd()+"\..")
from IntcodeClass import Intcode


pixel_map = {0: ' ',
              1: '|',
              2: 'X',
              3: '-',
              4: 'o'}
              
xl, xr, yb, yt = 0, 37, 0, 20

ai_x = [-1, -1] # [0]=ball, [1]=paddle

screen_buf = []
for y in range(yt+1):
    screen_buf.append(bytearray())
    for x in range(xr+1):
        screen_buf[y].append(ord(' '))

def redraw_screen(cpu):
    print("\033[?25l\033[0;0H", end='')
    score = ""
    pixels = {}
    while cpu.can_pop_output():
        x = cpu.pop_output()
        y = cpu.pop_output()
        t = cpu.pop_output()
        if t == 4: ai_x[0] = x
        if t == 3: ai_x[1] = x
        if x == -1 and y == 0: score = str(t)
        else: pixels[(x, y)] = t
        
    #xl, xr, yb, yt = get_screen_bounds(pixels)

    for pixel in pixels.keys():
        x, y = pixel
        t = pixels[pixel]
              
        screen_buf[y][x] = ord(pixel_map[t])
        
 
#    print("%d, %d, %d, %d" % (xl, xr, yb, yt))
    
#    print("len(pixels) == %d" % len(pixels))
    for yy in range(yb, yt+1):
        y = yt - yy
        print(screen_buf[y].decode())
#                print(pixel_map[pixels[(x, y)]], end='')
#            else:
#                print("%d, %d -> %d" % (x, y, t))
#                print("?", end='')
#        print("")
        
    print("score = %s" % score)
    print("ball_x = %d, paddle_x = %d" % (ai_x[0], ai_x[1]), flush=True)


def get_screen_bounds(pixels):

    xl, xr = None, None
    yb, yt = None, None
    
    for pixel in pixels.keys():
        x, y = pixel
        
        if xl is None: xl = x
        elif x < xl:  xl = x
        
        if xr is None: xr = x
        elif x > xr:  xr = x
        
        if yb is None: yb = y
        elif y < yb:  yb = y
        
        if yt is None: yt = y
        elif y > yt:  yt = y

    return xl, xr, yb, yt


def main():

    cpu = Intcode()
    
    opcodes = cpu.load_opcodes('input.txt')
    cpu.reset(opcodes)

    cpu.run()
    if not cpu.is_stopped(): raise("Program not stopped.")

    num_blocks = 0
    while cpu.can_pop_output():
        x = cpu.pop_output()
        y = cpu.pop_output()
        t = cpu.pop_output()
        
        if t == 2: num_blocks += 1
        
    print("num_blocks = %d" % (num_blocks))
    
    cpu.reset(opcodes)
    cpu._memory[0] = 2
    
    while True:

        cpu.run()
        redraw_screen(cpu)
        if cpu.is_stopped(): break
        
        #key = None
        #while key is None:
            #k = keyboard.read_event(suppress=True)
            #if k.name == 'q' and k.event_type == "down": sys.exit()
            #if k.name == 'z' and k.event_type == "down": key = -1
            #if k.name == 'x' and k.event_type == "down": key = 0
            #if k.name == 'c' and k.event_type == "down": key = 1
            #if k.name == 'space' and k.event_type == "down":
        time.sleep(0.01)
        
        if ai_x[0] == ai_x[1]: key =  0
        if ai_x[0] <  ai_x[1]: key = -1
        if ai_x[0] >  ai_x[1]: key =  1
            
        cpu.push_input(key)
        
        
    
    print("Game's over.")
    
    
    

if __name__ == "__main__":
    main()
