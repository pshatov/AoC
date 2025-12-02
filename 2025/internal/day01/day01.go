package day01

import (
	"fmt"
	"strconv"
)

const numDials = 100

func CountZeroes(lines []string) int {
	count := 0
	pos := 50
	for _, line := range lines {
		var dir int
		switch line[0] {
		case 'L':
			dir = -1
		case 'R':
			dir = 1
		default:
			panic(fmt.Sprintf("bad direction in line '%q'", line))
		}
		steps, err := strconv.Atoi(line[1:])
		if err != nil {
			panic(fmt.Sprintf("bad number of steps in line '%q'", line))
		}
		pos += dir * steps
		pos %= numDials
		if pos < 0 {
			pos += numDials
		}
		if pos == 0 {
			count++
		}
	}
	return count
}
