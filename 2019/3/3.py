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

    def __init__(self, x1, y1, x2,y2):
        self.a = WireSegmentPoint(x1, y1)
        self.b = WireSegmentPoint(x2, y2)

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
    def to_str(self):
        return "(%s, %s) - (%s, %s)" % (self.a.x, self.a.y, self.b.x, self.b.y)
        
    def check_cross(self, other_seg):
        
        if self.is_vertical and other_seg.is_vertical:
            if self.a.x == other_seg.a.x:
                yy_other = range(other_seg.min_y, other_seg.max_y+1)
                for y_self in range(self.min_y, self.max_y+1):
                    if y_self in yy_other:
                        return (self.a.x, y_self)
                
        if self.is_horizontal and other_seg.is_horizontal:
            if self.a.y == other_seg.a.y:
                xx_other = range(other_seg.min_x, other_seg.max_x+1)
                for x_self in range(self.min_x, self.max_x+1):
                    if x_self in xx_other:
                        return (x_self, self.a.y)
        
        if self.is_vertical and other_seg.is_horizontal:
            if other_seg.a.y in range(self.min_y, self.max_y+1) and self.a.x in range(other_seg.min_x, other_seg.max_x+1):
                return (self.a.x, other_seg.a.y)
        
        if self.is_horizontal and other_seg.is_vertical:
            if other_seg.a.x in range(self.min_x, self.max_x+1) and self.a.y in range(other_seg.min_y, other_seg.max_y+1):
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
        seg = WireSegment(old_x, old_y, new_x, new_y)
        segs.append(seg)
        old_x = new_x
        old_y = new_y
    return segs

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
