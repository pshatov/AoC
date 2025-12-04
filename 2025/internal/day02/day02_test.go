package day02

import (
	"aoc/2025/testutil"
	"strconv"
	"testing"

	"github.com/google/go-cmp/cmp"
)

func TestIsValidIDPart1(t *testing.T) {
	tests := []struct {
		id    int
		wants bool
	}{
		{111, true},
		{123, true},
		{55, false},
		{6464, false},
		{123123, false},
		{56, true},
		{6446, true},
		{123456, true},
	}
	for _, tc := range tests {
		t.Run(strconv.Itoa(tc.id), func(t *testing.T) {
			result := isValidIDPart1(tc.id)
			if result != tc.wants {
				t.Fatalf("isValidIDPart1(%d) result = %v, but wants = %v", tc.id, result, tc.wants)
			}
		})
	}
}

func TestIsValidIDPart2(t *testing.T) {
	tests := []struct {
		id    int
		wants bool
	}{
		{12341234, false},
		{123123123, false},
		{1212121212, false},
		{1111111, false},
		{123, true},
		{1234567890, true},
	}
	for _, tc := range tests {
		t.Run(strconv.Itoa(tc.id), func(t *testing.T) {
			result := isValidIDPart2(tc.id)
			if result != tc.wants {
				t.Fatalf("isValidIDPart2(%d) result = %v, but wants = %v", tc.id, result, tc.wants)
			}
		})
	}
}

func TestGetNextProbablyInvalidIDPart1(t *testing.T) {
	tests := []struct {
		id    int
		wants int
	}{
		{9, 11},
		{999, 1010},
		{99999, 100100},

		{10, 11},
		{1000, 1010},
		{100000, 100100},

		{99, 100},
		{9999, 10000},
		{999999, 1000000},

		{8, 11},
		{980, 1010},
		{998, 1010},
		{98000, 100100},
		{99998, 100100},

		{98, 99},
		{9800, 9898},
		{9899, 9999},
		{9988, 9999},
	}
	for _, tc := range tests {
		t.Run(strconv.Itoa(tc.id), func(t *testing.T) {
			result := getNextProbablyInvalidIDPart1(tc.id)
			if result != tc.wants {
				t.Fatalf("getNextProbablyInvalidID(%d) result = %v, but wants = %v", tc.id, result, tc.wants)
			}
		})
	}
}

func TestFindInvalidIDsPart1(t *testing.T) {
	tests := []struct {
		idRange string
		wants   []int
	}{
		{"11-22", []int{11, 22}},
		{"95-115", []int{99}},
		{"998-1012", []int{1010}},
		{"1188511880-1188511890", []int{1188511885}},
		{"222220-222224", []int{222222}},
		{"1698522-1698528", []int{}},
		{"446443-446449", []int{446446}},
		{"38593856-38593862", []int{38593859}},
	}
	for _, tc := range tests {
		t.Run(tc.idRange, func(t *testing.T) {
			result := findInvalidIDs(tc.idRange, isValidIDPart1, getNextProbablyInvalidIDPart1)
			if !cmp.Equal(result, tc.wants) {
				t.Fatalf("findInvalidIDs(%s) result = %v, but wants = %v", tc.idRange, result, tc.wants)
			}
		})
	}
}

func TestFindInvalidIDsPart2(t *testing.T) {
	tests := []struct {
		idRange string
		wants   []int
	}{
		{"11-22", []int{11, 22}},
		{"95-115", []int{99, 111}},
		{"998-1012", []int{999, 1010}},
		{"1188511880-1188511890", []int{1188511885}},
		{"222220-222224", []int{222222}},
		{"1698522-1698528", []int{}},
		{"446443-446449", []int{446446}},
		{"38593856-38593862", []int{38593859}},
		{"565653-565659", []int{565656}},
		{"824824821-824824827", []int{824824824}},
		{"2121212118-2121212124", []int{2121212121}},
	}
	for _, tc := range tests {
		t.Run(tc.idRange, func(t *testing.T) {
			result := findInvalidIDs(tc.idRange, isValidIDPart2, getNextProbablyInvalidIDPart2)
			if !cmp.Equal(result, tc.wants) {
				t.Fatalf("findInvalidIDs(%s) result = %v, but wants = %v", tc.idRange, result, tc.wants)
			}
		})
	}
}

func TestComputeInvalidIDs(t *testing.T) {
	example := testutil.ReadSingleLine(t, "example.txt")
	input := testutil.ReadSingleLine(t, "input.txt")

	tests := []struct {
		title      string
		line       string
		wantsPart1 int
		wantsPart2 int
	}{
		{"example", example, 1227775554, 4174379265},
		{"input", input, 31000881061, 46769308485},
	}

	for _, tc := range tests {
		t.Run(tc.title, func(t *testing.T) {
			resultV1 := ComputeInvalidIDsPart1(tc.line)
			if resultV1 != tc.wantsPart1 {
				t.Fatalf("ComputeInvalidIDsPart1(%s) result = %d, but wants = %d", tc.title, resultV1, tc.wantsPart1)
			}
			resultV2 := ComputeInvalidIDsPart2(tc.line)
			if resultV2 != tc.wantsPart2 {
				t.Fatalf("ComputeInvalidIDsV2(%s) result = %d, but wants = %d", tc.title, resultV2, tc.wantsPart2)
			}
		})
	}
}
