package day03

import (
	"aoc/2025/testutil"
	"testing"
)

func TestCalcMaxBankJoltage(t *testing.T) {
	tests := []struct {
		bank  string
		wants int
	}{
		{"987654321111111", 98},
		{"811111111111119", 89},
		{"234234234234278", 78},
		{"818181911112111", 92},
	}

	for _, tc := range tests {
		t.Run(tc.bank, func(t *testing.T) {
			result := calcMaxBankJoltage(tc.bank)
			if result != tc.wants {
				t.Fatalf("calcMaxBankJoltage(%s) result = %d, but wants = %d", tc.bank, result, tc.wants)
			}
		})
	}
}

func TestCalcTotalOutputJoltage(t *testing.T) {
	example := testutil.ReadAllLines(t, "example.txt")
	input := testutil.ReadAllLines(t, "input.txt")

	tests := []struct {
		title string
		banks []string
		wants int
	}{
		{"example", example, 357},
		{"input", input, 17144},
	}

	for _, tc := range tests {
		t.Run(tc.title, func(t *testing.T) {
			result := calcTotalOutputJoltage(tc.banks)
			if result != tc.wants {
				t.Fatalf("calcTotalOutputJoltage(%s) result = %d, but wants = %d", tc.title, result, tc.wants)
			}
		})
	}
}
