import os
import sys
import time
import keyboard

from enum import IntEnum

sys.path.append(os.getcwd()+"\..")
from IntcodeClass import Intcode

class MoveDirection(IntEnum):
    UP = 1
    DN = 2
    LT = 3
    RT = 4

class MoveStatus(IntEnum):
    HIT_WALL   = 0
    DID_MOVE   = 1
    SEE_OXYGEN = 2

class FieldPixel(IntEnum):
    UNKNOWN = 0
    EMPTY   = 1
    WALL    = 2
    OXYGEN  = 3

class Field():
    
    def __init__(self, W, H, X0, Y0):
        self._num_moves = 0
        self._pixels = []
        self._waves = []
        self._oxygen = []
        self._oxygen_new = []
        self._px = X0
        self._py = Y0
        for y in range(H):
            self._pixels.append([])
            self._waves.append([])
            self._oxygen.append([])
            self._oxygen_new.append([])
            for x in range(W):
                self._pixels[y].append(FieldPixel.UNKNOWN)
                self._waves[y].append(-1)
                self._oxygen[y].append(False)
                self._oxygen_new[y].append(False)
        self._pixels[self._py][self._px]= FieldPixel.EMPTY
        self._waves[self._py][self._px] = 0

    def pixel(self, x, y):
        return self._pixels[y][x]
        
    def wave(self, x, y):
        return self._waves[y][x]

    def oxygen(self, x, y):
        return self._oxygen[y][x]

    @property
    def px(self):
        return self._px
        
    @property
    def py(self):
        return self._py

    def is_explored_in_direction(self, d):
        x, y = self.calc_xy_in_direction(d)
        return self._pixels[y][x] != FieldPixel.UNKNOWN
    
    def calc_xy_in_direction(self, d):
        if   d == MoveDirection.UP: return self._px,   self._py-1
        elif d == MoveDirection.DN: return self._px,   self._py+1
        elif d == MoveDirection.LT: return self._px-1, self._py
        elif d == MoveDirection.RT: return self._px+1, self._py

    def calc_xy_in_direction_offset(self, x, y, d):
        if   d == MoveDirection.UP: return x,   y-1
        elif d == MoveDirection.DN: return x,   y+1
        elif d == MoveDirection.LT: return x-1, y
        elif d == MoveDirection.RT: return x+1, y

    def try_move_in_direction(self, d):
        s = _cpu_try_move(d)
        if s == MoveStatus.HIT_WALL:
            self.set_pixel_in_direction(d, FieldPixel.WALL)
        elif s == MoveStatus.DID_MOVE:
            self.set_pixel_in_direction(d, FieldPixel.EMPTY)
            _cpu_backtrack_move(d)
        elif s == MoveStatus.SEE_OXYGEN:
            self.set_pixel_in_direction(d, FieldPixel.OXYGEN)
            _cpu_backtrack_move(d)
        return s == MoveStatus.DID_MOVE

    def set_pixel_in_direction(self, d, v):
        x, y = self.calc_xy_in_direction(d)
        if self._pixels[y][x] != FieldPixel.UNKNOWN:
            #print("d = %s" % d)
            #print("v = %s" % v)
            #print("px / py = %d / %d" % (px, py))
            #print("x / y = %d / %d" % (x, y))
            #print("field[y][x] = %s" % self._pixels[y][x])
            raise Exception("Field overwrite!")
        self._pixels[y][x] = v
        
    def can_move_in_direction_cache(self, d):
        x, y = self.calc_xy_in_direction(d)
        if self._pixels[y][x] == FieldPixel.UNKNOWN:
            raise Exception("self._pixels[y][x] == FieldPixel.UNKNOWN")
        return self._pixels[y][x] == FieldPixel.EMPTY
    
    def move_in_direction(self, d, level):
        _cpu_just_move(d)
        self._px, self._py = self.calc_xy_in_direction(d)
        redraw_screen()
        self._num_moves += 1
        print("num_moves = %4d, recursion = %3d" % (self._num_moves, level))
        
    def repair_oxygen_system(self):
        for y in range(len(self._pixels)):
            for x in range(len(self._pixels[y])):
                if self._pixels[y][x] == FieldPixel.OXYGEN:
                    self._oxygen[y][x] = True
        
    def propagate_wave(self, w):
        found_oxygen = False
        for y in range(len(self._waves)):
            for x in range(len(self._waves[y])):
                if self._waves[y][x] == w:
                    found_oxygen = found_oxygen or self._propagate_wave_pixel(x, y, w)
        return found_oxygen
                    
    def _propagate_wave_pixel(self, x, y, w):
        for d in MoveDirection:
            tx, ty = self.calc_xy_in_direction_offset(x, y, d)
            if   self._pixels[ty][tx] == FieldPixel.OXYGEN: return True
            elif self._pixels[ty][tx] == FieldPixel.EMPTY:
                if self._waves[ty][tx] == -1:
                    self._waves[ty][tx] = w+1
        return False

    def _fill_oxygen_pixel(self, x, y):
        for d in MoveDirection:
            tx, ty = self.calc_xy_in_direction_offset(x, y, d)
            if self._pixels[ty][tx] == FieldPixel.EMPTY:
                if not self._oxygen[ty][tx]:
                    self._oxygen_new[ty][tx] = True

    def _propagate_oxygen(self):
        num_filled = 0
        for y in range(len(self._oxygen)):
            for x in range(len(self._oxygen[y])):
                if self._oxygen_new[y][x]:
                    self._oxygen_new[y][x] = False
                    self._oxygen[y][x] = True
                    num_filled += 1
        return num_filled == 0

    def fill_oxygen(self):
        for y in range(len(self._oxygen)):
            for x in range(len(self._oxygen[y])):
                if self._oxygen[y][x]:
                    self._fill_oxygen_pixel(x, y)
        return self._propagate_oxygen()

field_pixel_map = {FieldPixel.UNKNOWN: '?',
                   FieldPixel.EMPTY:   ' ',
                   FieldPixel.WALL:    '#',
                   FieldPixel.OXYGEN:  '*'}

W, H = 41, 41
X0, Y0 = 21, 21

field = Field(W, H, X0, Y0)

def redraw_screen():
    print("\033[?25l\033[0;0H", end='')
    for y in range(H):
        for x in range(W):
            if y == field.py and x == field.px:
                print("o", end='')
            else:
                print(field_pixel_map[field.pixel(x,y)], end='')
        print("")
    print("", flush=True)

def redraw_screen_wave():
    print("\033[?25l\033[0;0H", end='')
    for y in range(H):
        for x in range(W):
            pixel = field.pixel(x,y)
            pixel_map = field_pixel_map[pixel]
            wave = field.wave(x,y)
            if pixel == FieldPixel.EMPTY:
                if wave >= 0:
                    print("%d" % (wave % 10), end='')
                else:
                    print(pixel_map, end='')
            else:
                print(pixel_map, end='')
        print("")
    print("", flush=True)
    
def redraw_screen_oxygen():
    print("\033[?25l\033[0;0H", end='')
    for y in range(H):
        for x in range(W):
            pixel = field.pixel(x,y)
            pixel_map = field_pixel_map[pixel]
            oxygen = field.oxygen(x,y)
            if oxygen: print("O", end='')
            else:      print(pixel_map, end='')
        print("")
    print("", flush=True)    

def get_opposite_direction(d):
    if   d == MoveDirection.UP: return MoveDirection.DN
    elif d == MoveDirection.DN: return MoveDirection.UP
    elif d == MoveDirection.LT: return MoveDirection.RT
    elif d == MoveDirection.RT: return MoveDirection.LT


def _cpu_try_move(d):
    cpu.push_input(d)
    cpu.run()
    s = cpu.pop_output()
    return s

def _cpu_just_move(d):
    cpu.push_input(d)
    cpu.run()
    s = cpu.pop_output()
    if s != MoveStatus.DID_MOVE:
        raise Exception("s != MoveStatus.DID_MOVE")

def _cpu_backtrack_move(d):
    _cpu_just_move(get_opposite_direction(d))


def get_sideway_directions(d):
    if   d == MoveDirection.UP: return [MoveDirection.LT, MoveDirection.RT]
    elif d == MoveDirection.DN: return [MoveDirection.RT, MoveDirection.LT]
    elif d == MoveDirection.LT: return [MoveDirection.DN, MoveDirection.UP]
    elif d == MoveDirection.RT: return [MoveDirection.UP, MoveDirection.DN]

def wait_key():
    done = False
    while not done:
        k = keyboard.read_event(suppress=True)
        if k.name == 'x' and k.event_type == "down": sys.exit()
        done = k.name == 'space' and k.event_type == "down"
    
def can_move_sideways(d, dirs):
    if   d == MoveDirection.UP or d == MoveDirection.DN: return MoveDirection.LT in dirs or MoveDirection.RT in dirs
    elif d == MoveDirection.LT or d == MoveDirection.RT: return MoveDirection.UP in dirs or MoveDirection.DN in dirs


def field_look_around():
    dirs = []
    for d in MoveDirection:
        if field.is_explored_in_direction(d):
            if field.can_move_in_direction_cache(d): dirs.append(d)
        else:
            if field.try_move_in_direction(d): dirs.append(d)
            redraw_screen()
    return dirs

def explore_current_pixel(limit_dirs, level=0):
    can_go_dirs = field_look_around()
    for d in limit_dirs:
        if not d in can_go_dirs: continue
        queue = []
        went_distance = 0
        new_can_go_dirs = [d]
        while d in new_can_go_dirs:
            field.move_in_direction(d, level)
            went_distance += 1
            new_can_go_dirs = field_look_around()
            if can_move_sideways(d, new_can_go_dirs):
                queue.append(went_distance)
        while went_distance > 0:
            if went_distance in queue:
                new_can_go_dirs = field_look_around()
                sides = get_sideway_directions(d)
                dlt, drt = sides[0], sides[1]
                if dlt in new_can_go_dirs:
                    field.move_in_direction(dlt, level)
                    explore_current_pixel([dlt], level+1)
                    field.move_in_direction(drt, level)
                if drt in new_can_go_dirs:
                    field.move_in_direction(drt, level)
                    explore_current_pixel([drt], level+1)
                    field.move_in_direction(dlt, level)
            
            field.move_in_direction(get_opposite_direction(d), level)
            went_distance -= 1

cpu = Intcode()

def main():

    opcodes = cpu.load_opcodes('input.txt')
    cpu.reset(opcodes)
    
    init_dirs = []
    for d in MoveDirection:
        init_dirs.append(d)
    explore_current_pixel(init_dirs)
    
    wave = -1
    route_found = False
    redraw_screen_wave()
    while not route_found:
        wait_key()
        wave += 1
        route_found = field.propagate_wave(wave)
        redraw_screen_wave()
        
    print("")
    print("wave = %d" % (wave+1), flush=True)
    
    minutes = 0
    oxygen_filled = False
    field.repair_oxygen_system()
    redraw_screen_oxygen()
    while not oxygen_filled:
        wait_key()
        minutes += 1
        oxygen_filled = field.fill_oxygen()
        redraw_screen_oxygen()    

    print("")
    print("")
    print("minutes = %d" % (minutes-1), flush=True)


if __name__ == "__main__":
    main()
