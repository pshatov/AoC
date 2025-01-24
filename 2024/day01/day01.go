package day01

import (
	"fmt"
	"sort"
)

const Day = 1

func sortIDs(a []int) []int {
	aa := make([]int, len(a))
	copy(aa, a)
	sort.Ints(aa)
	return aa
}

func ComputeDistance(a, b []int) int {
	if len(a) != len(b) {
		panic(fmt.Errorf("a and b must be same length, but have %d and %d", len(a), len(b)))
	}
	sortedA := sortIDs(a)
	sortedB := sortIDs(b)
	total := 0
	for i := range sortedA {
		delta := sortedA[i] - sortedB[i]
		if delta < 0 {
			delta = -delta
		}
		total += delta
	}
	return total
}

func ComputeSimilarity(a, b []int) int {
	total := 0
	for _, idA := range a {
		coeff := 0
		for _, idB := range b {
			if idB == idA {
				coeff++
			}
		}
		total += idA * coeff
	}
	return total
}
