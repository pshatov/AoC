opcodes = list()
with open('input.txt') as f:
    line = f.readline().strip()
    line_parts = line.split(",")
    for line_part in line_parts:
        if len(line_part) > 0:
            opcodes.append(int(line_part))

def debug_dump_opcodes():
    i = 1
    for opcode in opcodes:
        print("%d" % opcode, end='')
        if i < len(opcodes): print(",", end='')
    print("")
    

pc = 0
run = True

#debug_dump_opcodes()

opcodes[1] = 12
opcodes[2] = 2

#debug_dump_opcodes()

while run:
    opcode = opcodes[pc]
    if opcode == 99:
        print("Stop.")
        run = False
    elif opcode == 1:
        a = opcodes[opcodes[pc+1]]
        b = opcodes[opcodes[pc+2]]
        s = a + b
        opcodes[opcodes[pc+3]] = s
        pc += 4
    elif opcode == 2:
        a = opcodes[opcodes[pc+1]]
        b = opcodes[opcodes[pc+2]]
        p = a * b
        opcodes[opcodes[pc+3]] = p
        pc += 4
    else:
        raise Exception("Bad opcode: %d." % (opcode))
        
    #debug_dump_opcodes()
        
print("opcodes[0] = %d" % opcodes[0])
