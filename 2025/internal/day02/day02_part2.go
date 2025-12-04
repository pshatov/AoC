package day02

import (
	"strconv"
)

func isValidIDPart2(idInt int) bool {
	idStr := strconv.Itoa(idInt)
	n := len(idStr)
	for size := 1; 2*size <= n; size++ {
		if n%size > 0 {
			continue
		}
		start := idStr[:size]
		valid := false
		for i := 1; i < n/size; i++ {
			repeat := idStr[i*size : (i+1)*size]
			if repeat != start {
				valid = true
				break
			}
		}
		if !valid {
			return false
		}
	}
	return true
}

func getNextProbablyInvalidIDPart2(idInt int) int {
	// TODO: try to write a better (faster) version
	return idInt + 1
}

func ComputeInvalidIDsPart2(idRanges string) int {
	return computeInvalidIDs(idRanges, isValidIDPart2, getNextProbablyInvalidIDPart2)
}
