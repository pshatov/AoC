from enum import IntEnum

class IntcodeInstr(IntEnum):
    STOP      = 99
    ADD       =  1
    MULT      =  2
    INPUT     =  3
    OUTPUT    =  4
    JMP_TRUE  =  5
    JMP_FALSE =  6
    CMP_LT    =  7
    CMP_EQ    =  8

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
            elif instr == IntcodeInstr.ADD:       self._handler_instr_add()
            elif instr == IntcodeInstr.MULT:      self._handler_instr_mult()
            elif instr == IntcodeInstr.INPUT:     self._handler_instr_input()
            elif instr == IntcodeInstr.OUTPUT:    self._handler_instr_output()
            elif instr == IntcodeInstr.JMP_TRUE:  self._handler_instr_jmp_true()
            elif instr == IntcodeInstr.JMP_FALSE: self._handler_instr_jmp_false()
            elif instr == IntcodeInstr.CMP_LT:    self._handler_instr_cmp_lt()
            elif instr == IntcodeInstr.CMP_EQ:    self._handler_instr_cmp_eq()
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
        if   instr == IntcodeInstr.ADD:       self._pc += 4
        elif instr == IntcodeInstr.MULT:      self._pc += 4
        elif instr == IntcodeInstr.INPUT:     self._pc += 2
        elif instr == IntcodeInstr.OUTPUT:    self._pc += 2
        elif instr == IntcodeInstr.JMP_TRUE:  self._pc += 3
        elif instr == IntcodeInstr.JMP_FALSE: self._pc += 3
        elif instr == IntcodeInstr.CMP_LT:    self._pc += 4
        elif instr == IntcodeInstr.CMP_EQ:    self._pc += 4
        else: raise Exception("_step_pc(): Unknown instr (%d)!" % instr)

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
        
    def _handler_instr_input(self):
        if self._input is None:
            raise Exception("_handler_opode_input() failed, since _input is None!")
        ptr = self._mem_at_pc_index(1)
        self._memory[ptr] = self._input
        self._step_pc(IntcodeInstr.INPUT)
        
    def _handler_instr_output(self):
        a_mode = self._decode_opcode_param_mode(1)
        a = self._get_param(1, a_mode)
        self._output.append(a)
        self._step_pc(IntcodeInstr.OUTPUT)

    def _handler_instr_jmp_true(self):
        a_mode = self._decode_opcode_param_mode(1)
        b_mode = self._decode_opcode_param_mode(2)
        
        a = self._get_param(1, a_mode)
        b = self._get_param(2, b_mode)
        
        if a != 0: self._pc = b
        else: self._step_pc(IntcodeInstr.JMP_TRUE)

    def _handler_instr_jmp_false(self):
        a_mode = self._decode_opcode_param_mode(1)
        b_mode = self._decode_opcode_param_mode(2)
        
        a = self._get_param(1, a_mode)
        b = self._get_param(2, b_mode)
        
        if a == 0: self._pc = b
        else: self._step_pc(IntcodeInstr.JMP_FALSE)

    def _handler_instr_cmp_lt(self):
        a_mode = self._decode_opcode_param_mode(1)
        b_mode = self._decode_opcode_param_mode(2)
        c_mode = self._decode_opcode_param_mode(3)
        
        if c_mode != IntcodeParamMode.POSITION:
            raise Exception("_handler_instr_cmp_lt() failed, since c_mode is %d!" % c_mode)
        
        a = self._get_param(1, a_mode)
        b = self._get_param(2, b_mode)
        c = 1 if a < b else 0
        
        c_addr = self._mem_at_pc_index(3)

        self._memory[c_addr] = c
        self._step_pc(IntcodeInstr.CMP_LT)

    def _handler_instr_cmp_eq(self):
        a_mode = self._decode_opcode_param_mode(1)
        b_mode = self._decode_opcode_param_mode(2)
        c_mode = self._decode_opcode_param_mode(3)
        
        if c_mode != IntcodeParamMode.POSITION:
            raise Exception("_handler_instr_cmp_lt() failed, since c_mode is %d!" % c_mode)
        
        a = self._get_param(1, a_mode)
        b = self._get_param(2, b_mode)
        c = 1 if a == b else 0
        
        c_addr = self._mem_at_pc_index(3)

        self._memory[c_addr] = c
        self._step_pc(IntcodeInstr.CMP_LT)

def load_opcodes(filename):
    opcodes = list()
    with open(filename) as f:
        line = f.readline().strip()
        line_parts = line.split(",")
        for line_part in line_parts:
            if len(line_part) > 0:
                opcodes.append(int(line_part))
    return opcodes

def check_codes(codes):
    ok = True
    num = len(codes)
    print("Number of output codes: %d" % num)
    for i in range(num):
        j = i + 1
        code = codes[i]
        if j < num:  code_ok = code == 0
        if j == num: code_ok = code != 0
        if code_ok: ok_str = "OK"
        else:       ok_str = "??"
        print("#%02d: [%s] %d " % (j, ok_str, code))
        if not code_ok: ok = False
    return ok
    
def print_codes(codes):
    num = len(codes)
    print("Number of output codes: %d" % num)
    for i in range(num):
        j = i + 1
        code = codes[i]
        print("#%02d: %d " % (j, code))

def main():
    cpu = Intcode()
    opcodes = load_opcodes('input.txt')

    cpu.reset(opcodes)
    cpu.set_input(1)
    result = cpu.run()
    codes = cpu.get_output()
    
    if not check_codes(codes): return

    cpu.reset(opcodes)
    cpu.set_input(5)
    result = cpu.run()
    codes = cpu.get_output()
    
    print_codes(codes)


if __name__ == "__main__":
    main()
