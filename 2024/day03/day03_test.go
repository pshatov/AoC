package day03_test

import (
	"fmt"
	"pshatov/aoc/year2024/day03"
	"pshatov/aoc/year2024/util"
	"testing"

	"github.com/stretchr/testify/assert"
)

func parseData(lines []string) (memory []day03.Instruction) {
	for _, ln := range lines {
		memory = append(memory, day03.Instruction(ln))
	}
	return
}

func TestComputation(t *testing.T) {
	for _, tc := range []struct {
		data                      string
		result, resultConditional int
	}{
		{"example_part1", 161, 0},
		{"example_part2", 0, 48},
		{"input", 178794710, 76729637},
	} {
		lines := util.LoadData(day03.Day, tc.data)
		instructions := parseData(lines)
		if tc.result > 0 {
			t.Run(
				fmt.Sprintf("TestCompute_%s", tc.data),
				func(t *testing.T) {
					n := 0
					for _, instr := range instructions {
						n += instr.Compute()
					}
					assert.Equal(t, tc.result, n)
				})
		}
		if tc.resultConditional > 0 {
			t.Run(
				fmt.Sprintf("TestComputeConditional_%s", tc.data),
				func(t *testing.T) {
					var total, part int
					enabled := true
					for _, instr := range instructions {
						part, enabled = instr.ComputeConditional(enabled)
						total += part
					}
					assert.Equal(t, tc.resultConditional, total)
				})
		}
	}
}
