from enum import IntEnum

class IntcodeOpcode(IntEnum):
    STOP   = 99
    ADD    =  1
    MULT   =  2
    INPUT  =  3
    OUTPUT =  4

class Intcode:

    def __init__(self):
        self._memory = None
        self._input = None
        self._output = []
        
    def reset(self, opcodes):
        self._memory = opcodes.copy()
        self._input = None
        self._output = []
        
    def run(self, opcodes=None):
    
        if not opcodes is None:
            self.reset(opcodes)
                
        pc = 0
        while(True):
            opcode = self._memory[pc]
            if   opcode == IntcodeOpcode.STOP: return self._memory[0]
            elif opcode == IntcodeOpcode.ADD:    pc = self._opcode_add(pc)
            elif opcode == IntcodeOpcode.MULT:   pc = self._opcode_mult(pc)
            elif opcode == IntcodeOpcode.INPUT:  pc = self._opcode_input(pc)
            elif opcode == IntcodeOpcode.OUTPUT: pc = self._opcode_output(pc)
            else: raise Exception("Bad opcode (%d)!" % opcode)

    def set_input(self, value):
        self._input = value
        
    def get_output(self):
        return self._output

    def _opcode_add(self, pc):
        #ptr_a = self._memory[pc+1]
        #ptr_b = self._memory[pc+2]
        #ptr_s = self._memory[pc+3]
        #a = self._memory[ptr_a]
        #b = self._memory[ptr_b]
        #s = a + b
        #self._memory[ptr_s] = s
        return pc + 4
        
    def _opcode_mult(self, pc):
        #ptr_a = self._memory[pc+1]
        #ptr_b = self._memory[pc+2]
        #ptr_p = self._memory[pc+3]
        #a = self._memory[ptr_a]
        #b = self._memory[ptr_b]
        #p = a * b
        #self._memory[ptr_p] = p
        return pc + 4
        
    def _opode_input(self, pc):
        #if self._input is None:
        #    raise("_opcode_input() failed, since _input is None!")
        #ptr = self._memory[pc+1]
        #self._memory[ptr] = _input
        return pc + 2
        
    def _opcode_output(self, pc):
        #ptr = self._memory[pc+1]
        #self._output = self._memory[ptr]
        return pc + 2

def load_opcodes(filename):
    opcodes = list()
    with open(filename) as f:
        line = f.readline().strip()
        line_parts = line.split(",")
        for line_part in line_parts:
            if len(line_part) > 0:
                opcodes.append(int(line_part))
    return opcodes

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
