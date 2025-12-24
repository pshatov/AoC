package day07

import (
	"aoc/2025/util"
	"testing"
)

func TestTachyonManifold(t *testing.T) {
	example := util.ReadAllLines("example.txt")
	input := util.ReadAllLines("input.txt")

	tests := []struct {
		title                  string
		lines                  []string
		wantsPart1, wantsPart2 int
	}{
		{"example", example, 21, 40},
		{"input", input, 1553, 15811946526915},
	}

	for _, tc := range tests {
		t.Run("part1_"+tc.title, func(t *testing.T) {
			result := CalcNumSplits(tc.lines)
			if result != tc.wantsPart1 {
				t.Fatalf("CalcNumSplits(%s) result = %d, but tc.wants = %d", tc.title, result, tc.wantsPart1)
			}
		})
		t.Run("part2_"+tc.title, func(t *testing.T) {
			result := CalcNumTimelines(tc.lines)
			if result != tc.wantsPart2 {
				t.Fatalf("CalcNumTimelines(%s) result = %d, but tc.wants = %d", tc.title, result, tc.wantsPart2)
			}
		})
	}
}
