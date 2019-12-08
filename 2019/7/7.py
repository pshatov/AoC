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

class IntcodeParamMode(IntEnum):
    POSITION  = 0
    IMMEDIATE = 1

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
        
    def reset(self, opcodes):
        self._pc = 0
        self._memory = opcodes.copy()
        self._input = []
        self._output = []
        self._state = IntcodeState.IDLE
        
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
            else: raise Exception("Unknown instruction (%d)!" % instr)

    def _mem_at_pc(self):
        return self._memory[self._pc]

    def _mem_at_pc_index(self, index):
        return self._memory[self._pc+index]

    def clear_input(self):
        self._input = []

    def push_input(self, value):
        self._input.append(value)

    def pop_output(self):
        return self._output.pop(0)

    def is_waiting_input(self):
        return self._state == IntcodeState.WAIT_INPUT

    def is_stopped(self):
        return self._state == IntcodeState.STOPPED        

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
            self._state = IntcodeState.WAIT_INPUT
            return True
        ptr = self._mem_at_pc_index(1)
        value = self._input.pop(0)
        self._memory[ptr] = value
        self._step_pc(IntcodeInstr.INPUT)
        return False
        
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

def gen_phase_permuts(phase_set):
    
    # there's nothing to generate when we only have a single element
    if len(phase_set) == 1: return [phase_set]
    
    # start with an empty list
    result = []
    for i in range(len(phase_set)):
    
        # fix one of the phases from the set
        fixed_phase = phase_set[i]
        
        # generate a subset of all the remaining phases
        phase_subset = phase_set.copy()
        phase_subset.remove(fixed_phase)
        
        # recursively generate all the permutations of the subset
        sub_permuts = gen_phase_permuts(phase_subset)
        
        # glue our fixed phase to the list of the subset permutations
        for next_sub_permut in sub_permuts:
            result.append([fixed_phase] + next_sub_permut)

    # done
    return result        

def print_phase_permut(phase_permut):
    for i in range(len(phase_permut)):
        if i == 0: print("[", end='')
        else: print(", ", end='')
        print("%d" % phase_permut[i], end='')
    if i == (len(phase_permut)-1): print("]: ", end='')

def all_cpus_stopped(cpus):
    for i in range(len(cpus)):
        if not cpus[i].is_stopped(): return False
    return True
    
def main():

    # load opcodes
    opcodes = load_opcodes('input.txt')

    # create processor, create phase list
    cpu = Intcode()
    phases = [0, 1, 2, 3, 4]
    
    # generate permutations
    phase_permuts = gen_phase_permuts(phases)

    # find largest achievable power
    max_pwr = None
    for next_phase_permut in phase_permuts:
    
        print_phase_permut(next_phase_permut)
    
        # the very first amplifier's input is 0
        value_in = 0
        for i in range(len(next_phase_permut)):
            
            # reset cpu
            cpu.reset(opcodes)
            
            # set input parameters (phase and value)
            cpu.push_input(next_phase_permut[i])
            cpu.push_input(value_in)
            
            # run program
            cpu.run()
            
            # get output value and feed it into the next amplifier
            value_out = cpu.pop_output()
            value_in = value_out
        
        # store largest seen power
        if max_pwr is None:       max_pwr = value_out
        elif value_out > max_pwr: max_pwr = value_out
            
        # print intermediate result
        print("%d (max: %d)" % (value_out, max_pwr))
    
    # print final result
    print("max_pwr = %d" % max_pwr)

    # create processors, create phase list
    cpus = []
    phases = [5, 6, 7, 8, 9]
    
    # generate phase permutations, create processors
    phase_permuts = gen_phase_permuts(phases)
    for i in range(len(phases)): cpus.append(Intcode())

    # find largest achievable power
    max_pwr = None
    for next_phase_permut in phase_permuts:
    
        print_phase_permut(next_phase_permut)
    
        # reset all the processors and feed them with their phase offsets
        for i in range(len(cpus)):
            cpus[i].reset(opcodes)
            cpus[i].push_input(next_phase_permut[i])
        
        # the very first input is zero
        prev_cpu_output = 0
        
        # run all the processors until they're stopped
        cpu_index = 0
        while True:
            
            # set current processor's input
            cpus[cpu_index].push_input(prev_cpu_output)
            cpus[cpu_index].run()
            
            # the current processor is either stalled due to lack of input
            # or stopped altogether
            prev_cpu_output = cpus[cpu_index].pop_output()
                        
            # stop once all the loop is finished
            if all_cpus_stopped(cpus): break

            # goto next processor
            cpu_index += 1
            if cpu_index == len(cpus): cpu_index = 0

        # store largest seen power
        if max_pwr is None:             max_pwr = prev_cpu_output
        elif prev_cpu_output > max_pwr: max_pwr = prev_cpu_output
            
        # print intermediate result
        print("%d (max: %d)" % (prev_cpu_output, max_pwr))
    
    # print final result
    print("max_pwr = %d" % max_pwr)


if __name__ == "__main__":
    main()
