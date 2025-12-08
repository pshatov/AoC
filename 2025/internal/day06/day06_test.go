package day06

import (
	"aoc/2025/util"
	"testing"
)

func TestCalcHomework(t *testing.T) {
	example := util.ReadAllLines("example.txt")
	input := util.ReadAllLines("input.txt")

	tests := []struct {
		title                  string
		homework               []string
		wantsPart1, wantsPart2 int
	}{
		{"example", example, 4277556, 3263827},
		{"input", input, 6100348226985, -1},
	}

	for _, tc := range tests {
		t.Run(tc.title+"_part1", func(t *testing.T) {
			result := CalcHomework(tc.homework, false)
			if result != tc.wantsPart1 {
				t.Fatalf("CalcHomework(%s) result = %d, but tc.wants = %d", tc.title, result, tc.wantsPart1)
			}
		})
		t.Run(tc.title+"_part2", func(t *testing.T) {
			result := CalcHomework(tc.homework, true)
			if result != tc.wantsPart2 {
				t.Fatalf("CalcHomework(%s) result = %d, but tc.wants = %d", tc.title, result, tc.wantsPart2)
			}
		})
	}
}
