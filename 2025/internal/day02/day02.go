package day02

import (
	"fmt"
	"strconv"
	"strings"
)

func isValidID(idInt int) bool {
	idStr := strconv.Itoa(idInt)
	n := len(idStr)
	if n%2 > 0 {
		return true
	}
	return idStr[:n/2] != idStr[n/2:]
}

func getNextProbablyInvalidID(idInt int) int {
	idStr := strconv.Itoa(idInt)
	n := len(idStr)
	if n%2 > 0 {
		nextID := 1
		for i := range n {
			nextID *= 10
			if i == n/2 {
				nextID += 1
			}
		}
		return nextID
	}

	upperStr, lowerStr := idStr[:n/2], idStr[n/2:]
	upperInt, err := strconv.Atoi(upperStr)
	if err != nil {
		panic(fmt.Sprintf("bad upper part of id '%s'", idStr))
	}
	lowerInt, err := strconv.Atoi(lowerStr)
	if err != nil {
		panic(fmt.Sprintf("bad lower part of id '%s'", idStr))
	}

	nextUpperInt := upperInt + 1
	if upperInt > lowerInt {
		nextUpperInt = upperInt
	} else if len(strconv.Itoa(nextUpperInt)) > n/2 {
		nextID := nextUpperInt
		for range n / 2 {
			nextID *= 10
		}
		return nextID
	}
	nextID := nextUpperInt
	for range n / 2 {
		nextID *= 10
	}
	nextID += nextUpperInt
	return nextID
}

func findInvalidIDs(idRange string) []int {
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
		ok := isValidID(beginInt)
		if !ok {
			result = append(result, beginInt)
		}
		beginInt = getNextProbablyInvalidID(beginInt)
		if beginInt > endInt {
			break
		}
	}
	return result
}

func ComputeInvalidIDs(idRanges string) int {
	total := 0
	parts := strings.SplitSeq(idRanges, ",")
	for p := range parts {
		invalidIDs := findInvalidIDs(p)
		for _, id := range invalidIDs {
			total += id
		}
	}
	return total
}
