package day05

import (
	"aoc/2025/util"
	"testing"
)

func TestCalcFreshIngredients(t *testing.T) {
	example := ParseDatabase(util.ReadAllLines("example.txt"))
	input := ParseDatabase(util.ReadAllLines("input.txt"))

	tests := []struct {
		title                  string
		db                     Database
		wantsPart1, wantsPart2 int
	}{
		{"example", example, 3, 14},
		{"input", input, 690, 344323629240733},
	}

	for _, tc := range tests {
		t.Run(tc.title, func(t *testing.T) {
			result := CalcFreshIngredients(tc.db)
			if result != tc.wantsPart1 {
				t.Fatalf("CalcFreshIngredients(%s) result = %d, but tc.wants = %d", tc.title, result, tc.wantsPart1)
			}
		})
		t.Run(tc.title, func(t *testing.T) {
			result := CalcFreshRanges(tc.db.FreshRanges)
			if result != tc.wantsPart2 {
				t.Fatalf("CalcFreshRanges(%s) result = %d, but tc.wants = %d", tc.title, result, tc.wantsPart2)
			}
		})
	}
}
