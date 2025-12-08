package day06

import (
	"aoc/2025/util"
	"testing"
)

func TestCalcHomework(t *testing.T) {
	example := util.ReadAllLines("example.txt")
	input := util.ReadAllLines("input.txt")

	tests := []struct {
		title    string
		homework []string
		wants    int
	}{
		{"example", example, 4277556},
		{"input", input, 6100348226985},
	}

	for _, tc := range tests {
		t.Run(tc.title, func(t *testing.T) {
			result := CalcHomework(tc.homework)
			if result != tc.wants {
				t.Fatalf("CalcHomework(%s) result = %d, but tc.wants = %d", tc.title, result, tc.wants)
			}
		})
	}
}
