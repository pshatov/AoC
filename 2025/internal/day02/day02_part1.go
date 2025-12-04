package day02

import (
	"fmt"
	"strconv"
)

func isValidIDPart1(idInt int) bool {
	idStr := strconv.Itoa(idInt)
	n := len(idStr)
	if n%2 > 0 {
		return true
	}
	return idStr[:n/2] != idStr[n/2:]
}

func getNextProbablyInvalidIDPart1(idInt int) int {
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

func ComputeInvalidIDsPart1(idRanges string) int {
	return computeInvalidIDs(idRanges, isValidIDPart1, getNextProbablyInvalidIDPart1)
}
