package day01_test

import (
	"aoc/2025/internal/day01"
	"aoc/2025/testutil"
	"testing"
)

func TestCountZeroes(t *testing.T) {
	example := testutil.ReadLines(t, "example.txt")
	input := testutil.ReadLines(t, "input.txt")

	tests := []struct {
		title string
		lines []string
		want  int
	}{
		{"example", example, 3},
		{"input", input, 1102},
	}

	for _, tc := range tests {
		t.Run(tc.title, func(t *testing.T) {
			got := day01.CountZeroes(tc.lines)
			if got != tc.want {
				t.Fatalf("CountZeroes(%s) = %d, but want = %d", tc.title, got, tc.want)
			}
		})
	}
}
