package day03

import (
	"aoc/2025/util"
	"fmt"
	"testing"
)

func TestCalcMaxBankJoltage(t *testing.T) {
	tests := []struct {
		bank  string
		num   int
		wants int
	}{
		{"987654321111111", 2, 98},
		{"811111111111119", 2, 89},
		{"234234234234278", 2, 78},
		{"818181911112111", 2, 92},

		{"987654321111111", 12, 987654321111},
		{"811111111111119", 12, 811111111119},
		{"234234234234278", 12, 434234234278},
		{"818181911112111", 12, 888911112111},
	}

	for _, tc := range tests {
		name := fmt.Sprintf("%s:%d", tc.bank, tc.num)
		t.Run(name, func(t *testing.T) {
			result := calcMaxBankJoltage(tc.bank, tc.num)
			if result != tc.wants {
				t.Fatalf("calcMaxBankJoltage(%s, %d) result = %d, but wants = %d", tc.bank, tc.num, result, tc.wants)
			}
		})
	}
}

func TestCalcTotalOutputJoltage(t *testing.T) {
	example := util.ReadAllLines("example.txt")
	input := util.ReadAllLines("input.txt")

	tests := []struct {
		title string
		banks []string
		num   int
		wants int
	}{
		{"example", example, 2, 357},
		{"input", input, 2, 17144},
		{"example", example, 12, 3121910778619},
		{"input", input, 12, 170371185255900},
	}

	for _, tc := range tests {
		name := fmt.Sprintf("%s:%d", tc.title, tc.num)
		t.Run(name, func(t *testing.T) {
			result := calcTotalOutputJoltage(tc.banks, tc.num)
			if result != tc.wants {
				t.Fatalf("calcTotalOutputJoltage(%s, %d) result = %d, but wants = %d", tc.title, tc.num, result, tc.wants)
			}
		})
	}
}
