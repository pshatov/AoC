package day12

import (
	"fmt"
	"strconv"
	"strings"
)

const (
	opcodeInvalid = iota
	opcodeCpy     = iota
	opcodeInc     = iota
	opcodeDec     = iota
	opcodeJnz     = iota
)

const (
	regInvalid = iota
	regA       = iota
	regB       = iota
	regC       = iota
	regD       = iota
)

var opcodeLut = map[string]int{
	"cpy": opcodeCpy,
	"inc": opcodeInc,
	"dec": opcodeDec,
	"jnz": opcodeJnz,
}

var regLut = map[string]int{
	"a": regA,
	"b": regB,
	"c": regC,
	"d": regD,
}

type ProgramStr []string

type RegState struct {
	A, B, C, D int
}

type instrOperand struct {
	literal bool
	value   int
}

type decodedInstruction struct {
	opcode   int
	op1, op2 instrOperand
}

func panicBadRegister(reg string) {
	panic(fmt.Sprintf("bad register '%v'", reg))
}

func panicBadLiteral(value string) {
	panic(fmt.Sprintf("bad literal '%v'", value))
}

func panicBadOpcode(opcode string) {
	panic(fmt.Sprintf("bad opcode '%v'", opcode))
}

func panicBadOperand(operand string) {
	panic(fmt.Sprintf("bad operand '%v'", operand))
}

func tryParseReg(field string) (instrOperand, bool) {
	reg, ok := regLut[field]
	if !ok {
		return instrOperand{}, false
	}
	return instrOperand{false, reg}, true
}

func tryParseLiteral(field string) (instrOperand, bool) {
	value, err := strconv.Atoi(field)
	if err != nil {
		return instrOperand{}, false
	}
	return instrOperand{true, value}, true
}

func tryParseRegOrLiteral(field string) (instrOperand, bool) {
	var op instrOperand
	var ok bool
	op, ok = tryParseReg(field)
	if ok {
		return op, true
	}
	op, ok = tryParseLiteral(field)
	if ok {
		return op, true
	}
	return instrOperand{}, false
}

func parseInstructionStr(instr string) *decodedInstruction {

	decodedInstr := decodedInstruction{}

	fields := strings.Fields(instr)
	if len(fields) < 2 {
		panic(fmt.Sprintf("bad instruction '%v', less than two fields", instr))
	}

	opcode, ok := opcodeLut[fields[0]]
	if !ok {
		panicBadOpcode(fields[0])
	}
	decodedInstr.opcode = opcode
	fields = fields[1:]

	var ok1, ok2 bool
	switch opcode {
	case opcodeCpy:
		if len(fields) != 2 {
			panic(fmt.Sprintf("bad copy instruction, needs two opcodes, but has %v", len(fields)))
		}
		decodedInstr.op1, ok1 = tryParseRegOrLiteral(fields[0])
		decodedInstr.op2, ok2 = tryParseReg(fields[1])
		if !ok1 {
			panicBadOperand(fields[0])
		}
		if !ok2 {
			panicBadRegister(fields[1])
		}

	case opcodeInc:
		fallthrough
	case opcodeDec:
		if len(fields) != 1 {
			panic(fmt.Sprintf("bad increment/decrement instruction, needs one opcode, but has %v", len(fields)))
		}
		decodedInstr.op1, ok1 = tryParseReg(fields[0])
		if !ok1 {
			panicBadRegister(fields[0])
		}

	case opcodeJnz:
		if len(fields) != 2 {
			panic(fmt.Sprintf("bad jnz instruction, needs two opcodes, but has %v", len(fields)))
		}
		decodedInstr.op1, ok1 = tryParseRegOrLiteral(fields[0])
		decodedInstr.op2, ok2 = tryParseLiteral(fields[1])
		if !ok1 {
			panicBadRegister(fields[0])
		}
		if !ok2 {
			panicBadLiteral(fields[1])
		}

	default:
		panic("internal opcode dispatch error")
	}

	return &decodedInstr
}

func (state *RegState) getRegPtr(op instrOperand) *int {

	if op.literal {
		panic("can't get pointer to literal operand")
	}

	switch op.value {
	case regA:
		return &state.A
	case regB:
		return &state.B
	case regC:
		return &state.C
	case regD:
		return &state.D
	default:
		panic("can't get pointer, invalid operand")
	}
}

func (state *RegState) runIncrement(op instrOperand) {
	ptr := state.getRegPtr(op)
	value := *ptr
	*ptr = value + 1
}

func (state *RegState) runDecrement(op instrOperand) {
	ptr := state.getRegPtr(op)
	value := *ptr
	*ptr = value - 1
}

func (state *RegState) runCopy(opSrc instrOperand, opDst instrOperand) {
	var value int
	if opSrc.literal {
		value = opSrc.value
	} else {
		ptr := state.getRegPtr(opSrc)
		value = *ptr
	}

	ptr := state.getRegPtr(opDst)
	*ptr = value
}

func (state *RegState) runJumpIfNotZero(opCondition instrOperand, opValue instrOperand) (jumpValue int, jumpFlag bool) {
	if !opValue.literal {
		panic("jump value must be literal")
	}
	jumpValue = opValue.value

	var value int
	if opCondition.literal {
		value = opCondition.value
	} else {
		ptr := state.getRegPtr(opCondition)
		value = *ptr
	}

	jumpFlag = value != 0

	return
}

func (state *RegState) runInstructionStr(instr string) (jumpValue int, jumpFlag bool) {

	decodedInstr := parseInstructionStr(instr)

	switch decodedInstr.opcode {
	case opcodeCpy:
		state.runCopy(decodedInstr.op1, decodedInstr.op2)

	case opcodeInc:
		state.runIncrement(decodedInstr.op1)

	case opcodeDec:
		state.runDecrement(decodedInstr.op1)

	case opcodeJnz:
		jumpValue, jumpFlag = state.runJumpIfNotZero(decodedInstr.op1, decodedInstr.op2)

	default:
		panic("tried to execute unknown opcode")
	}

	return
}

func RunProgram(prog ProgramStr, state *RegState) {

	// TODO: First parse everything, then run (currently the code has to parse every time, but
	//       it can jump to already parsed instructions)

	ptr, stop := 0, false
	for !stop {

		if ptr < 0 || ptr >= len(prog) {
			panic("bad instruction pointer!")
		}

		jumpValue, jumpFlag := state.runInstructionStr(prog[ptr])
		if !jumpFlag {
			ptr++
		} else {
			ptr += jumpValue
		}

		if ptr == len(prog) {
			stop = true
		}
	}
}
