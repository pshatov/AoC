import os
import sys
import keyboard

sys.path.append(os.getcwd()+"\..")
from IntcodeClass import Intcode

field = []
cpu = Intcode()

DIR_SYMS = ["^", "v", "<", ">"]

class Robot():
        
    def wake_up(self, x, y, dir):
        self._x = x
        self._y = y
        self._dir = dir
        
    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y
        
    @property
    def dir(self):
        return self._dir
        
    def _xy_forward(self):
        if   self._dir == "^": return self._x,   self._y-1
        elif self._dir == "v": return self._x,   self._y+1
        elif self._dir == "<": return self._x-1, self._y
        elif self._dir == ">": return self._x+1, self._y
        raise Exception("self._dir = '%s'" % self._dir)
        
    def _xy_left(self):
        if   self._dir == "^": return self._x-1, self._y
        elif self._dir == "v": return self._x+1, self._y
        elif self._dir == "<": return self._x,   self._y+1
        elif self._dir == ">": return self._x,   self._y-1
        raise Exception("self._dir = '%s'" % self._dir)
    
    def _xy_right(self):
        if   self._dir == "^": return self._x+1, self._y
        elif self._dir == "v": return self._x-1, self._y
        elif self._dir == "<": return self._x,   self._y-1
        elif self._dir == ">": return self._x,   self._y+1
        raise Exception("self._dir = '%s'" % self._dir)

    def _field_left(self):
        x, y = self._xy_left()
        return field[y][x]
        
    def _field_right(self):
        x, y = self._xy_right()
        return field[y][x]
        
    def _field_forward(self):
        x, y = self._xy_forward()
        return field[y][x]
        
    def need_turn(self):
        if self._field_forward() == "#": return "1"
        else:
            if self._field_left() == "#": return "L"
            if self._field_right() == "#": return "R"
            return ""
            
    def handle_instr(self, instr):
        if instr == "1":
            self._x, self._y = self._xy_forward()
        elif instr == "L":
            if   self._dir == "^": self._dir = "<"
            elif self._dir == "v": self._dir = ">"
            elif self._dir == "<": self._dir = "v"
            elif self._dir == ">": self._dir = "^"
        elif instr == "R":
            if   self._dir == "^": self._dir = ">"
            elif self._dir == "v": self._dir = "<"
            elif self._dir == "<": self._dir = "^"
            elif self._dir == ">": self._dir = "v"            

robot = Robot()

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


prog = []
def prog_append(instr):
    if   instr == "L": prog.append(instr)
    elif instr == "R": prog.append(instr)
    elif instr == "1":
        if prog[-1].isdigit(): prog[-1] = str(int(prog[-1]) + 1)
        else: prog.append(instr)
    robot.handle_instr(instr)

def prog_print():
    print("")
    for i in range(len(prog)):
        if i > 0: print(",", end='')
        print("%s" % prog[i], end='')
    print("", flush=True)

def reprint_field():
    _vt100_cursor_xy(0, 0)
    for y in range(len(field)):
        for x in range(len(field[y])):
            if robot.y == y and robot.x == x:
                print("%s" % robot.dir, end='')
                pass
            else:
                print("%s" % field[y][x], end='')
        print("")
    print("", flush=True)

def find_repeats(s, l):
    repeats = []
    num_possible_offsets = len(s) - 2 * l + 1
    for offset in range(num_possible_offsets):
        offset_end = offset + l
        pattern = s[offset:offset_end]
        rest = s[offset_end:]
        if pattern in rest and pattern not in repeats:
            repeats.append(pattern)
    return repeats
    
    
    
    

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
            
    for i in range(len(field)):
        field[i] = "." + field[i] + "."

    field.insert(0, "."*len(field[0]))
    field.append("."*len(field[0]))
            
    field_y = len(field)
    field_x = len(field[0])
    
    for y in range(field_y):
        for x in range(field_x):
            if field[y][x] in DIR_SYMS:
                robot.wake_up(x, y, field[y][x])
                fc = field[y][x]
                field[y] = field[y].replace(fc, "#")

    reprint_field()

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
                #wait_key()
                xy = (x, y)
                junctions.append(xy)
                _vt100_cursor_xy(x, y)
                print("O", end='', flush=True)
            
        _vt100_cursor_xy(0, field_y)
        
    s = 0
    for j in junctions:
        jx, jy = j[0], j[1]
        s += jx * jy
        
    print("s = %d" % s, flush=True)
        
    while True:
        #wait_key()
        z = robot.need_turn()
        if z == "": break
        prog_append(z)
        reprint_field()
        prog_print()

    
    lr_prog = ""
    lr_dict = {}
    
    for i in range(0, len(prog), 2):
        a = prog[i]
        b = prog[i+1]
        ab = "%s,%s" % (a, b)
        if not ab in lr_dict.keys():
            lr_dict[ab] = str(len(lr_dict.keys()) + 1)
        lr_prog += str(list(lr_dict.keys()).index(ab)+1)
            
    print("")
    print("LR-dictionary:")
    for k in lr_dict.keys():
        print("'%s' -> '%s'" % (k, lr_dict[k]))
    print("")
    print("LR-program: %s (%d)" % (lr_prog, len(lr_prog)))

    
    abc_full_dict = []
    for l in range(len(lr_prog) // 2, 1, -1):
        abc_full_dict += find_repeats(lr_prog, l)
    
    a_dict = []
    b_dict = []
    c_dict = []
    
    for a in abc_full_dict:
        lr_begin = lr_prog[0:len(a)];
        if a == lr_begin: a_dict.append(a)

    for c in abc_full_dict:
        lr_end = lr_prog[-len(c):];
        if c == lr_end: c_dict.append(c)
    
    for d in abc_full_dict:
        if d in a_dict: continue
        if d in c_dict: continue
        b_dict.append(d)
    
    print("A-dictionary: ", end='')
    for i in range(len(a_dict)):
        if i > 0: print(", ", end='')
        print(a_dict[i], end='')
    print("")
    print("C-dictionary: ", end='')
    for i in range(len(c_dict)):
        if i > 0: print(", ", end='')
        print(c_dict[i], end='')
    print("")
    print("B-dictionary: ", end='')
    for i in range(len(b_dict)):
        if i > 0: print(", ", end='')
        print(b_dict[i], end='')
    print("")

    solution = []
    print("")
    print("Compressing...")
    for a in a_dict:
        sa = lr_prog
        #print("A-word:     '%7s' > " % a, end='')
        sa = sa.replace(a, " | A | ")
        while "|  |" in sa: sa = sa.replace("|  |", "|")
        sa = sa.strip()
        #print("s = %s" % sa)
        for c in c_dict:
            sc = sa
            #print("  C-word:   '%7s' > " % c, end='')
            sc = sc.replace(c, " | C | ")
            while "|  |" in sc: sc = sc.replace("|  |", "|")
            sc = sc.strip()
            #print("s = %s" % sc)
            for b in b_dict:
                sb = sc
                #print("    B-word: '%7s' > " % b, end='')
                sb = sb.replace(b, " | B | ")
                while "|  |" in sb: sb = sb.replace("|  |", "|")
                sb = sb.strip()
                #print("s = %s" % sb)
                
                s = sb
                s = s.replace("|", "")
                s = s.replace(" ", "")
                s0 = s
                s = s.replace("A", "")
                s = s.replace("B", "")
                s = s.replace("C", "")
                
                if len(s) == 0:
                    abc0 = a, b, c, s0
                    solution.append(abc0)
                    print("Found solution: '%s'" % s0)
                    print("  A = '%s'" % a)
                    print("  B = '%s'" % b)
                    print("  C = '%s'" % c)
    
    if len(solution) != 1:
        raise Exception("len(solution) == %d" % len(solution))
    
    a = solution[0][0]
    b = solution[0][1]
    c = solution[0][2]
    s = solution[0][3]
    print("")
    print("Formatting programs...")
    
    main_routine = ""
    a_routine = ""
    b_routine = ""
    c_routine = ""
    for i in range(len(s)):
        if i > 0: main_routine += ","
        main_routine += s[i]
    main_routine += "\n"
    
    for i in range(len(a)):
        if i > 0: a_routine += ","
        for lr in lr_dict.keys():
            if lr_dict[lr] == a[i]:
                a_routine += lr
    a_routine += "\n"

    for i in range(len(b)):
        if i > 0: b_routine += ","
        for lr in lr_dict.keys():
            if lr_dict[lr] == b[i]:
                b_routine += lr
    b_routine += "\n"

    for i in range(len(c)):
        if i > 0: c_routine += ","
        for lr in lr_dict.keys():
            if lr_dict[lr] == c[i]:
                c_routine += lr
    c_routine += "\n"
    
    print("Main routine: %s" % main_routine, end='')
    print("A-routine: %s" % a_routine, end='')
    print("B-routine: %s" % b_routine, end='')
    print("C-routine: %s" % c_routine, end='')
    
    print("")
    print("Waking up robot...", flush=True)
    print ("  opcodes[0] = %d" % opcodes[0])
    opcodes[0] = 2
    print ("  opcodes[0] = %d" % opcodes[0])
    cpu.reset(opcodes)

    print("")
    print("Overriding robot movement logic...", flush=True)
    for i in range(len(main_routine)):
        cpu.push_input(ord(main_routine[i]))
    for i in range(len(a_routine)):
        cpu.push_input(ord(a_routine[i]))
    for i in range(len(b_routine)):
        cpu.push_input(ord(b_routine[i]))
    for i in range(len(c_routine)):
        cpu.push_input(ord(c_routine[i]))
    
    print("")
    print("Turning off live video feed to save resources...", flush=True)
    cpu.push_input(ord("n"))
    cpu.push_input(ord("\n"))
        
    print("")
    print("Collecting dust ", end='', flush=True)
    cpu.run()
    if not cpu.is_stopped: raise Exception("not cpu.is_stopped!")
    
    while True:
        dust = cpu.pop_output()            
        
        if cpu.can_pop_output():
            print(".", end='', flush=True)
        else: break
    print(" %d" % dust)
        
    
    
    
    
if __name__ == "__main__":
    main()
