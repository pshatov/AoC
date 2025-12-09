package day07

import (
	"aoc/2025/util"
	"testing"
)

func TestCalcNumSplits(t *testing.T) {
	example := util.ReadAllLines("example.txt")
	input := util.ReadAllLines("input.txt")

	tests := []struct {
		title                  string
		lines                  []string
		wantsPart1, wantsPart2 int
	}{
		{"example", example, 21, -1},
		{"input", input, 1553, -1},
	}

	for _, tc := range tests {
		t.Run("part1_"+tc.title, func(t *testing.T) {
			result := CalcNumSplits(tc.lines)
			if result != tc.wantsPart1 {
				t.Fatalf("CalcNumSplits(%s) result = %d, but tc.wants = %d", tc.title, result, tc.wantsPart1)
			}
		})
		// t.Run(tc.title+"_part2", func(t *testing.T) {
		// 	result := CalcHomework(tc.homework, true)
		// 	if result != tc.wantsPart2 {
		// 		t.Fatalf("CalcHomework(%s) result = %d, but tc.wants = %d", tc.title, result, tc.wantsPart2)
		// 	}
		// })
	}
}
