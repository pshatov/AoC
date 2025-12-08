package day06

import (
	"fmt"
	"strconv"
	"strings"
)

func CalcHomework(lines []string) int {
	n := len(lines) - 1
	numbers := make([][]int, n)
	signs := make([]string, 0)
	for y, ln := range lines {
		fields := strings.Fields(ln)
		if y < n {
			numbers[y] = make([]int, len(fields))
			for x, f := range fields {
				num, err := strconv.Atoi(f)
				if err != nil {
					panic(fmt.Sprintf("can't parse homework line %d, bad field '%s'", y, f))
				}
				if y < n {
					numbers[y][x] = num
				}
			}
		}
		if y == n {
			signs = append(signs, fields...)
		}
	}

	total := 0
	for x := range len(signs) {
		op := signs[x]
		temp := numbers[0][x]
		for y := 1; y < n; y++ {
			switch op {
			case "+":
				temp += numbers[y][x]
			case "*":
				temp *= numbers[y][x]
			}
		}
		next := total + temp
		if next < total {
			panic("overflow")
		}
		total = next
	}
	return total
}
