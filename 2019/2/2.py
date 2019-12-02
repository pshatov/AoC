from enum import IntEnum

class IntcodeOpcode(IntEnum):
    STOP = 99
    ADD  =  1
    MULT =  2

class Intcode:

    def __init__(self):
        self._memory = None
        
    def reset(self, opcodes):
        self._memory = opcodes.copy()
        
    def run(self, opcodes=None):
    
        if not opcodes is None:
            self.reset(opcodes)
                
        pc = 0
        while(True):
            opcode = self._memory[pc]
            if   opcode == IntcodeOpcode.STOP: return self._memory[0]
            elif opcode == IntcodeOpcode.ADD:  pc = self._opcode_add(pc)
            elif opcode == IntcodeOpcode.MULT: pc = self._opcode_mult(pc)
            else: raise Exception("Bad opcode (%d)!" % opcode)

    def _opcode_add(self, pc):
        ptr_a = self._memory[pc+1]
        ptr_b = self._memory[pc+2]
        ptr_s = self._memory[pc+3]
        a = self._memory[ptr_a]
        b = self._memory[ptr_b]
        s = a + b
        self._memory[ptr_s] = s
        return pc + 4
        
    def _opcode_mult(self, pc):
        ptr_a = self._memory[pc+1]
        ptr_b = self._memory[pc+2]
        ptr_p = self._memory[pc+3]
        a = self._memory[ptr_a]
        b = self._memory[ptr_b]
        p = a * b
        self._memory[ptr_p] = p
        return pc + 4
    
def load_opcodes(filename):
    opcodes = list()
    with open(filename) as f:
        line = f.readline().strip()
        line_parts = line.split(",")
        for line_part in line_parts:
            if len(line_part) > 0:
                opcodes.append(int(line_part))
    return opcodes
    
def find_xy(cpu, opcodes, target):
    for x in range(100):
        for y in range(100):
            opcodes_try = opcodes.copy()
            opcodes_try[1] = x
            opcodes_try[2] = y
            ret = cpu.run(opcodes_try)
            if ret == target: return (x, y)
        print(".", end='')
        if x % 10 == 9: print("")
    
def main():
    cpu = Intcode()
    opcodes = load_opcodes('input.txt')

    opcodes_patch = opcodes.copy()
    opcodes_patch[1] = 12
    opcodes_patch[2] = 2
    
    cpu.reset(opcodes_patch)
    result = cpu.run()
    
    print("%d" % result)
    
    (x, y) = find_xy(cpu, opcodes, 19690720)
    z = x * 100 + y
    
    print("noun = %d, verb = %d (%d)" % (x, y, z))


if __name__ == "__main__":
    main()
