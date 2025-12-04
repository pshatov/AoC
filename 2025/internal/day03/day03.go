package day03

import (
	"fmt"
	"strconv"
)

func getIndividualJoltages(bank string) []int {
	values := make([]int, len(bank))
	for pos := 0; pos < len(bank); pos++ {
		value, err := strconv.Atoi(string(bank[pos]))
		if err != nil {
			panic(fmt.Sprintf("could not parse bank=%s at pos=%d", bank, pos))
		}
		values[pos] = value
	}
	return values
}

func calcMaxBankJoltage(bank string) int {
	values := getIndividualJoltages((bank))
	max := 0
	for i := 0; i < len(values)-1; i++ {
		for j := i + 1; j < len(values); j++ {
			temp := 10*values[i] + values[j]
			if temp > max {
				max = temp
			}
		}
	}

	return max
}

func calcTotalOutputJoltage(banks []string) int {
	total := 0
	for _, b := range banks {
		total += calcMaxBankJoltage(b)
	}
	return total
}
