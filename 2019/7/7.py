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
        self._input = []
        self._output = []
        
    def reset(self, opcodes):
        self._pc = 0
        self._memory = opcodes.copy()
        self._input = []
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

    def clear_input(self):
        self._input = []

    def append_input(self, value):
        self._input.append(value)

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
        if len(self._input) == 0:
            raise Exception("_handler_opode_input() failed, since _input is empty!")
        ptr = self._mem_at_pc_index(1)
        value = self._input.pop(0)
        self._memory[ptr] = value
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

def calc_vars(array):
    if len(array) == 1: return [array]
    ret = []
    for i in range(len(array)):
        fix_element = array[i]
        sub_array = array.copy()
        sub_array.remove(fix_element)
        sub_vars = calc_vars(sub_array)
        for next_sub_var in sub_vars:
            ret.append([fix_element] + next_sub_var)
    return ret
        
        
        
    
        

def main():
    cpu = Intcode()
    opcodes = load_opcodes('input.txt')

    phases = [0, 1, 2, 3, 4]
    vars = calc_vars(phases)

    max_pwr = None
    for next_var in vars:
        val_in = 0
        for i in range(len(next_var)):
            if i == 0: print("[", end='')
            else: print(", ", end='')
            print("%d" % next_var[i], end='')
            if i == (len(next_var)-1): print("]: ", end='')
            cpu.reset(opcodes)
            cpu.clear_input()
            cpu.append_input(next_var[i])
            cpu.append_input(val_in)
            cpu.run()
            val_out = cpu.get_output()
            val_out = val_out[0]
            val_in = val_out
        
        if max_pwr is None:     max_pwr = val_out
        elif val_out > max_pwr: max_pwr = val_out
            
        print("%d (max: %d)" % (val_out, max_pwr))
    
    print("max_pwr = %d" % max_pwr)

    #cpu.reset(opcodes)
    #cpu.set_input(1)
    
    #result = cpu.run()
    #codes = cpu.get_output()
    
    #if not check_codes(codes): return

    #cpu.reset(opcodes)
    #cpu.set_input(5)
    #result = cpu.run()
    #codes = cpu.get_output()
    
    #print_codes(codes)


if __name__ == "__main__":
    main()
