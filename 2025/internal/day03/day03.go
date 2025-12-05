package day03

import (
	"fmt"
	"strconv"
)

func calcMaxBankJoltage(bank string, num int) int {
	result := []byte{}
	extra := len(bank) - num
	for i := range len(bank) {
		b := bank[i]
		for extra > 0 && len(result) > 0 && result[len(result)-1] < b {
			result = result[:len(result)-1]
			extra--
		}
		result = append(result, b)
	}
	for extra > 0 {
		result = result[:len(result)-1]
		extra--
	}
	total, err := strconv.Atoi(string(result))
	if err != nil {
		panic(fmt.Errorf("internal error: %w", err))
	}
	return total
}

func calcTotalOutputJoltage(banks []string, num int) int {
	total := 0
	for _, b := range banks {
		total += calcMaxBankJoltage(b, num)
	}
	return total
}
