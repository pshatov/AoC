import re

fmt = re.compile('^(\d+)\-(\d+) ([a-z])\: ([a-z]+).*$')

DB = []
with open('input.txt') as f:
    for fl in f:
        DB.append(fl.strip())


num_valid = 0
for row in DB:
    
    m = re.fullmatch(fmt, row)
    if m is None:
        raise RuntimeError("Can't parse: '%s'!" % row)
    
    min, max, char, pwd = m.group(1, 2, 3, 4)
    
    min, max = int(min), int(max)
    
    cnt = pwd.count(char)
    if min <= cnt <= max:
        num_valid += 1
        
print("num_valid: %d" % num_valid)


num_valid = 0
for row in DB:
    
    m = re.fullmatch(fmt, row)
    if m is None:
        raise RuntimeError("Can't parse: '%s'!" % row)
    
    min, max, char, pwd = m.group(1, 2, 3, 4)
    
    min, max = int(min), int(max)
    if (pwd[min-1] == char) != (pwd[max-1] == char):
        num_valid += 1
    
print("num_valid: %d" % num_valid)
