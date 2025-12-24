package day08

import (
	"aoc/2025/util"
	"testing"
)

func TestJunctionBoxes(t *testing.T) {
	example := parseLines(util.ReadAllLines("example.txt"))
	input := parseLines(util.ReadAllLines("input.txt"))

	tests := []struct {
		title                  string
		boxes                  []util.XYZ
		count                  int
		wantsPart1, wantsPart2 int
	}{
		{"example", example, 10, 40, -1},
		{"input", input, 1000, 50568, -1},
	}

	for _, tc := range tests {
		t.Run("part1_"+tc.title, func(t *testing.T) {
			result := CalcPart1(tc.boxes, tc.count)
			if result != tc.wantsPart1 {
				t.Fatalf("CalcPart1(%s) result = %d, but tc.wants = %d", tc.title, result, tc.wantsPart1)
			}
		})
		// t.Run("part2_"+tc.title, func(t *testing.T) {
		// 	result := CalcNumTimelines(tc.lines)
		// 	if result != tc.wantsPart2 {
		// 		t.Fatalf("CalcNumTimelines(%s) result = %d, but tc.wants = %d", tc.title, result, tc.wantsPart2)
		// 	}
		// })
	}
}
