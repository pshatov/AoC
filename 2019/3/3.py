line1 = ""
line2 = ""
with open('input.txt') as f:
    line1 = f.readline().strip()
    line2 = f.readline().strip()

class WireSegmentPoint:
    
    def __init__(self, x, y):
        self.x = x
        self.y = y

class WireSegment:

    def __init__(self, x1, y1, x2, y2, dir, len):
        self.a = WireSegmentPoint(x1, y1)
        self.b = WireSegmentPoint(x2, y2)
        self.dir = dir
        self.len = len

    @property
    def min_x(self):
        return min(self.a.x, self.b.x)
    
    @property
    def max_x(self):
        return max(self.a.x, self.b.x)
    
    @property
    def min_y(self):
        return min(self.a.y, self.b.y)
        
    @property
    def max_y(self):
        return max(self.a.y, self.b.y)
        
    @property
    def is_vertical(self):
        return self.a.x == self.b.x
        
    @property
    def is_horizontal(self):
        return self.a.y == self.b.y

    @property
    def range_x(self):
        return range(self.min_x, self.max_x+1)
    
    @property
    def range_y(self):
        return range(self.min_y, self.max_y+1)
        
    def check_contains(self, cross):
        return cross[0] in self.range_x and cross[1] in self.range_y
        
    def check_cross(self, other_seg):
        
        if self.is_vertical and other_seg.is_vertical:
            if self.a.x == other_seg.a.x:
                for y_self in self.range_y:
                    if y_self in other_seg.range_y:
                        return (self.a.x, y_self)
                
        if self.is_horizontal and other_seg.is_horizontal:
            if self.a.y == other_seg.a.y:
                for x_self in self.range_x:
                    if x_self in other_seg.range_x:
                        return (x_self, self.a.y)
        
        if self.is_vertical and other_seg.is_horizontal:
            if other_seg.a.y in self.range_y and self.a.x in other_seg.range_x:
                return (self.a.x, other_seg.a.y)
        
        if self.is_horizontal and other_seg.is_vertical:
            if other_seg.a.x in self.range_x and self.a.y in other_seg.range_y:
                return (other_seg.a.x, self.a.y)

def get_wire_segments(line):
    segs = []
    old_x = 0
    old_y = 0
    line_segs = line.split(",")
    for line_seg in line_segs:
        line_seg_dir = line_seg[:1]
        line_seg_len = int(line_seg[1:])
        new_x = old_x
        new_y = old_y
        if   line_seg_dir == "D": new_y -= line_seg_len
        elif line_seg_dir == "U": new_y += line_seg_len
        elif line_seg_dir == "L": new_x -= line_seg_len
        elif line_seg_dir == "R": new_x += line_seg_len
        else: raise Exception("Bad segment_direction ('%s')!" % line_seg_dir)
        seg = WireSegment(old_x, old_y, new_x, new_y, line_seg_dir, line_seg_len)
        segs.append(seg)
        old_x = new_x
        old_y = new_y
    return segs

def calc_steps(segs, cross):
    x = 0
    y = 0
    
    steps = 0
    for next_seg in segs:
        for i in range(next_seg.len):
            if   next_seg.dir == "D": y -= 1
            elif next_seg.dir == "U": y += 1
            elif next_seg.dir == "L": x -= 1
            elif next_seg.dir == "R": x += 1
            else: raise Exception("Bad segment direction ('%s')!" % next_seg.dir)
            steps += 1
            if x == cross[0] and y == cross[1]:
                return steps
    raise Exception("calc_steps() failed...")

segs1 = get_wire_segments(line1)
segs2 = get_wire_segments(line2)

crosses = []
for next_seg1 in segs1:
    for next_seg2 in segs2:
        cross = next_seg1.check_cross(next_seg2)
        if not cross is None:
            if cross[0] != 0 or cross[1] != 0:
                crosses.append(cross)

i = 0
for next_cross in crosses:
    dist = abs(next_cross[0]) + abs(next_cross[1])
    if i == 0:            min_dist = dist
    elif dist < min_dist: min_dist = dist
    i += 1
    
print("min_dist = %d" % min_dist)

i = 0
for next_cross in crosses:
    steps1 = calc_steps(segs1, next_cross)
    steps2 = calc_steps(segs2, next_cross)
    steps = steps1 + steps2
    if i == 0:              min_steps = steps
    elif steps < min_steps: min_steps = steps
    i += 1
    print("%d + %d = %d [min: %d]" % (steps1, steps2, steps, min_steps))

print("min_steps = %d" % min_steps)
