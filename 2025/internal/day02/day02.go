package day02

import (
	"fmt"
	"strconv"
	"strings"
)

func findInvalidIDs(
	idRange string,
	validator func(int) bool,
	generator func(int) int,
) []int {
	result := []int{}
	rangeParts := strings.Split(idRange, "-")
	if len(rangeParts) != 2 {
		panic(fmt.Sprintf("bad id range '%s'", idRange))
	}
	beginStr, endStr := rangeParts[0], rangeParts[1]
	beginInt, err := strconv.Atoi(beginStr)
	if err != nil {
		panic(fmt.Sprintf("bad id range begin '%s'", beginStr))
	}
	endInt, err := strconv.Atoi(endStr)
	if err != nil {
		panic(fmt.Sprintf("bad id range end '%s'", endStr))
	}
	for {
		ok := validator(beginInt)
		if !ok {
			result = append(result, beginInt)
		}
		beginInt = generator(beginInt)
		if beginInt > endInt {
			break
		}
	}
	return result
}

func computeInvalidIDs(
	idRanges string,
	validator func(int) bool,
	generator func(int) int,
) int {
	total := 0
	parts := strings.SplitSeq(idRanges, ",")
	for p := range parts {
		invalidIDs := findInvalidIDs(p, validator, generator)
		for _, id := range invalidIDs {
			total += id
		}
	}
	return total
}
