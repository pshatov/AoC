package day03

import (
	"regexp"
	"strconv"
)

const Day = 3

const (
	instrNop int = iota
	instrDo
	instrDont
	instrMul
)

var (
	mulRE  = regexp.MustCompile(`mul\((\d{1,3}),(\d{1,3})\)`)
	doRE   = regexp.MustCompile(`do\(\)`)
	dontRE = regexp.MustCompile(`don't\(\)`)
)

type reEntry struct {
	re   *regexp.Regexp
	enum int
}

var allREs = []reEntry{
	{doRE, instrDo},
	{dontRE, instrDont},
	{mulRE, instrMul},
}

type Instruction string

func (i Instruction) Compute() int {
	parts := mulRE.FindAllStringSubmatch(string(i), -1)
	total := 0
	for _, p := range parts {
		a, _ := strconv.Atoi(p[1])
		b, _ := strconv.Atoi(p[2])
		total += a * b
	}
	return total
}

func (i Instruction) ComputeConditional(enabled bool) (int, bool) {
	total := 0
	keepGoing := true
	data := []byte(i)
	cache := make(map[int][]int)
	for keepGoing {
		firstInstr := instrNop
		firstOffset := len(data)
		firstLength := 0

		for _, nextRE := range allREs {
			m := nextRE.re.FindSubmatchIndex(data)
			if m != nil {
				if m[0] < firstOffset {
					firstInstr = nextRE.enum
					firstOffset = m[0]
					firstLength = m[1] - m[0]
				}
				cache[nextRE.enum] = m
			}
		}

		switch firstInstr {
		case instrNop:
			keepGoing = false
		case instrDo:
			enabled = true
		case instrDont:
			enabled = false
		case instrMul:
			if enabled {
				a, _ := strconv.Atoi(string(data[cache[instrMul][2]:cache[instrMul][3]]))
				b, _ := strconv.Atoi(string(data[cache[instrMul][4]:cache[instrMul][5]]))
				total += a * b
			}
		}

		if keepGoing {
			data = data[firstOffset+firstLength:]
		}
	}
	return total, enabled
}
