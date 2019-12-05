from enum import IntEnum

class IntcodeInstr(IntEnum):
    STOP   = 99
    ADD    =  1
    MULT   =  2
    INPUT  =  3
    OUTPUT =  4

class IntcodeParamMode(IntEnum):
    POSITION  = 0
    IMMEDIATE = 1

class Intcode:

    def __init__(self):
        self._pc = 0
        self._memory = None
        self._input = None
        self._output = []
        
    def reset(self, opcodes):
        self._pc = 0
        self._memory = opcodes.copy()
        self._input = None
        self._output = []
        
    def run(self):
        while(True):
            instr = self._decode_opcode_instr()
            if   instr == IntcodeInstr.STOP: return self._memory[0]
            elif instr == IntcodeInstr.ADD:    self._handler_instr_add()
            elif instr == IntcodeInstr.MULT:   self._handler_instr_mult()
            elif instr == IntcodeInstr.INPUT:  self._handler_instr_input()
            elif instr == IntcodeInstr.OUTPUT: self._handler_instr_output()
            else: raise Exception("Unknown instruction (%d)!" % instr)

    def _mem_at_pc(self):
        return self._memory[self._pc]

    def _mem_at_pc_index(self, index):
        return self._memory[self._pc+index]

    def set_input(self, value):
        self._input = value

    def get_output(self):
        return self._output            

    def _decode_opcode_instr(self):
        opcode = self._mem_at_pc()
        if opcode < 0:
            raise Exception("Bad opcode (%d)!" % opcode)
        instr = opcode % 100
        return instr

    def _decode_opcode_param_mode(self, index):
        opcode = self._mem_at_pc()
        opcode //= 100
        for i in range(1, index):
            opcode //= 10
        mode = opcode % 10
        return mode
    
    def _get_param(self, index, mode):
        mem_value = self._mem_at_pc_index(index)
        if   mode == IntcodeParamMode.POSITION:  return self._memory[mem_value]
        elif mode == IntcodeParamMode.IMMEDIATE: return mem_value
        else: raise Exception("Unknown parameter mode (%d)!" % mode)

    def _step_pc(self, instr):
        if   instr == IntcodeInstr.ADD:    self._pc += 4
        elif instr == IntcodeInstr.MULT:   self._pc += 4
        elif instr == IntcodeInstr.INPUT:  self._pc += 2
        elif instr == IntcodeInstr.OUTPUT: self._pc += 2

    def _handler_instr_add(self):
        a_mode = self._decode_opcode_param_mode(1)
        b_mode = self._decode_opcode_param_mode(2)
        c_mode = self._decode_opcode_param_mode(3)
        
        if c_mode != IntcodeParamMode.POSITION:
            raise Exception("_handler_instr_add() failed, since c_mode is %d!" % c_mode)
        
        a = self._get_param(1, a_mode)
        b = self._get_param(2, b_mode)
        c = a + b
        
        c_addr = self._mem_at_pc_index(3)

        self._memory[c_addr] = c
        self._step_pc(IntcodeInstr.ADD)
        
    def _handler_instr_mult(self):
        a_mode = self._decode_opcode_param_mode(1)
        b_mode = self._decode_opcode_param_mode(2)
        c_mode = self._decode_opcode_param_mode(3)
        
        if c_mode != IntcodeParamMode.POSITION:
            raise Exception("_handler_instr_mult() failed, since c_mode is %d!" % c_mode)
        
        a = self._get_param(1, a_mode)
        b = self._get_param(2, b_mode)
        c = a * b
        
        c_addr = self._mem_at_pc_index(3)

        self._memory[c_addr] = c
        self._step_pc(IntcodeInstr.MULT)
        
    # def _opode_input(self, pc):

        # ???

        # #if self._input is None:
        # #    raise("_opcode_input() failed, since _input is None!")
        # #ptr = self._memory[pc+1]
        # #self._memory[ptr] = _input
        # return pc + 2
        
    # def _opcode_output(self, pc):
        
        # ???
        
        # #ptr = self._memory[pc+1]
        # #self._output = self._memory[ptr]
        # return pc + 2

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
            cpu.reset(opcodes_try)
            ret = cpu.run()
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
