package day04

import (
	"aoc/2025/util"
	"testing"
)

func TestCalcAccessibleRolls(t *testing.T) {
	example := util.ReadAllLines("example.txt")
	input := util.ReadAllLines("input.txt")

	tests := []struct {
		title string
		maze  []string
		wants int
	}{
		{"example", example, 13},
		{"input", input, 1320},
	}

	for _, tc := range tests {
		t.Run(tc.title, func(t *testing.T) {
			num := CalcAccessibleRolls(tc.maze)
			if num != tc.wants {
				t.Fatalf("CalcAccessibleRolls(%s) result = %d, but wants = %d", tc.title, num, tc.wants)
			}
		})
	}
}
