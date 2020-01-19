from enum import Enum, IntEnum, auto

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
    OFFSET    =  9

class IntcodeParamMode(IntEnum):
    POSITION  = 0
    IMMEDIATE = 1
    RELATIVE  = 2

class IntcodeState(Enum):
    IDLE       = auto()
    WAIT_INPUT = auto()
    STOPPED    = auto()

class Intcode:

    def __init__(self):
        self._pc = 0
        self._memory = None
        self._input = []
        self._output = []
        self._state = IntcodeState.IDLE
        self._offset = 0
        
    def reset(self, opcodes):
        self._pc = 0
        self._memory = opcodes.copy()
        self._input = []
        self._output = []
        self._state = IntcodeState.IDLE
        self._offset = 0
        
    def run(self):
        while True:
            instr = self._decode_opcode_instr()
            if   instr == IntcodeInstr.STOP:
                self._state = IntcodeState.STOPPED
                return
            elif instr == IntcodeInstr.ADD: self._handler_instr_add()
            elif instr == IntcodeInstr.MULT: self._handler_instr_mult()
            elif instr == IntcodeInstr.INPUT:
                wait = self._handler_instr_input()
                if wait: return
            elif instr == IntcodeInstr.OUTPUT: self._handler_instr_output()
            elif instr == IntcodeInstr.JMP_TRUE: self._handler_instr_jmp_true()
            elif instr == IntcodeInstr.JMP_FALSE: self._handler_instr_jmp_false()
            elif instr == IntcodeInstr.CMP_LT: self._handler_instr_cmp_lt()
            elif instr == IntcodeInstr.CMP_EQ: self._handler_instr_cmp_eq()
            elif instr == IntcodeInstr.OFFSET: self._handler_instr_offset()
            else: raise Exception("Unknown instruction (%d)!" % instr)

    def _prealloc_mem(self, length):
        while length >= len(self._memory):
            self._memory.append(0)
            
    def _get_mem_at_pc(self):
        self._prealloc_mem(self._pc)
        return self._memory[self._pc]

    def _get_mem_at_pc_index(self, index):
        self._prealloc_mem(self._pc + index)
        return self._memory[self._pc + index]

    def _get_mem_at_offset(self, offset):
        self._prealloc_mem(offset)
        return self._memory[offset]

    def _set_mem_at_offset(self, offset, value):
        self._prealloc_mem(offset)
        self._memory[offset] = value

    def clear_input(self):
        self._input = []

    def push_input(self, value):
        self._input.append(value)

    def pop_output(self):
        return self._output.pop(0)
        
    def can_pop_output(self):
        return len(self._output) > 0

    def is_waiting_input(self):
        return self._state == IntcodeState.WAIT_INPUT

    def is_stopped(self):
        return self._state == IntcodeState.STOPPED        

    def _decode_opcode_instr(self):
        opcode = self._get_mem_at_pc()
        if opcode < 0:
            raise Exception("Bad opcode (%d)!" % opcode)
        instr = opcode % 100
        return instr

    def _decode_opcode_param_mode(self, index):
        opcode = self._get_mem_at_pc()
        opcode //= 100
        for i in range(1, index):
            opcode //= 10
        mode = opcode % 10
        return mode
    
    def _get_param_value(self, index):
        mode = self._decode_opcode_param_mode(index)
        mem_value = self._get_mem_at_pc_index(index)
        if mode == IntcodeParamMode.IMMEDIATE: return mem_value
        else:
            address = self._get_param_address(index)
            if   mode == IntcodeParamMode.POSITION: return self._get_mem_at_offset(address)
            elif mode == IntcodeParamMode.RELATIVE: return self._get_mem_at_offset(address)
            else: raise Exception("_get_param_value(): Unknown parameter mode (%d)!" % mode)
        
    def _get_param_address(self, index):
        mode = self._decode_opcode_param_mode(index)
        mem_value = self._get_mem_at_pc_index(index)
        if   mode == IntcodeParamMode.POSITION: return mem_value
        elif mode == IntcodeParamMode.RELATIVE: return self._offset + mem_value
        else: raise Exception("_get_param_address(): Unknown parameter mode (%d)!" % mode)

    def _step_pc(self, instr):
        if   instr == IntcodeInstr.ADD:       self._pc += 4
        elif instr == IntcodeInstr.MULT:      self._pc += 4
        elif instr == IntcodeInstr.INPUT:     self._pc += 2
        elif instr == IntcodeInstr.OUTPUT:    self._pc += 2
        elif instr == IntcodeInstr.JMP_TRUE:  self._pc += 3
        elif instr == IntcodeInstr.JMP_FALSE: self._pc += 3
        elif instr == IntcodeInstr.CMP_LT:    self._pc += 4
        elif instr == IntcodeInstr.CMP_EQ:    self._pc += 4
        elif instr == IntcodeInstr.OFFSET:    self._pc += 2
        else: raise Exception("_step_pc(): Unknown instr (%d)!" % instr)

    def _handler_instr_add(self):
        a = self._get_param_value(1)
        b = self._get_param_value(2)
        c = a + b
        
        c_addr = self._get_param_address(3)

        self._set_mem_at_offset(c_addr, c)
        self._step_pc(IntcodeInstr.ADD)
        
    def _handler_instr_mult(self):
        a = self._get_param_value(1)
        b = self._get_param_value(2)
        c = a * b
        
        c_addr = self._get_param_address(3)

        self._set_mem_at_offset(c_addr, c)
        self._step_pc(IntcodeInstr.MULT)
        
    def _handler_instr_input(self):        
        if len(self._input) == 0:
            self._state = IntcodeState.WAIT_INPUT
            return True
        
        a_mode = self._decode_opcode_param_mode(1)

        if a_mode == IntcodeParamMode.POSITION:
            ptr = self._get_mem_at_pc_index(1)
        if a_mode == IntcodeParamMode.RELATIVE:
            ptr = self._offset + self._get_mem_at_pc_index(1)
            
        value = self._input.pop(0)
        self._set_mem_at_offset(ptr, value)
        
        self._step_pc(IntcodeInstr.INPUT)
        return False
        

        
    def _handler_instr_output(self):    
        a = self._get_param_value(1)
        self._output.append(a)
        self._step_pc(IntcodeInstr.OUTPUT)

    def _handler_instr_jmp_true(self):        
        a_mode = self._decode_opcode_param_mode(1)
        b_mode = self._decode_opcode_param_mode(2)
        
        a = self._get_param_value(1)
        b = self._get_param_value(2)
        
        if a != 0: self._pc = b
        else: self._step_pc(IntcodeInstr.JMP_TRUE)

    def _handler_instr_jmp_false(self):        
        a = self._get_param_value(1)
        b = self._get_param_value(2)
        
        if a == 0: self._pc = b
        else: self._step_pc(IntcodeInstr.JMP_FALSE)

    def _handler_instr_cmp_lt(self):        
        a = self._get_param_value(1)
        b = self._get_param_value(2)
        c = 1 if a < b else 0
        
        c_addr = self._get_param_address(3)

        self._set_mem_at_offset(c_addr, c)
        self._step_pc(IntcodeInstr.CMP_LT)

    def _handler_instr_cmp_eq(self):        
        a = self._get_param_value(1)
        b = self._get_param_value(2)
        c = 1 if a == b else 0
        
        c_addr = self._get_param_address(3)

        self._set_mem_at_offset(c_addr, c)
        self._step_pc(IntcodeInstr.CMP_LT)
    
    def _handler_instr_offset(self):
        old_offset = self._offset
                
        a = self._get_param_value(1)
        
        self._offset += a

        self._step_pc(IntcodeInstr.OFFSET)
        
        new_offset = self._offset
        


    def load_opcodes(self, filename):
        opcodes = list()
        with open(filename) as f:
            line = f.readline().strip()
            line_parts = line.split(",")
            for line_part in line_parts:
                if len(line_part) > 0:
                    opcodes.append(int(line_part))
        return opcodes     

