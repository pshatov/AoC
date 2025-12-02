package day01

import (
	"fmt"
	"strconv"
)

const numDials = 100

func updatePos(oldPos int, dir int, steps int, final *int, total *int) int {

	*total += steps / numDials
	steps %= numDials

	if steps == 0 {
		if oldPos == 0 {
			*final++
		}
		return oldPos
	}

	newPos := oldPos + dir*steps
	if newPos < 0 {
		newPos += numDials
		if oldPos > 0 {
			*total++
		}
	} else if newPos == 0 {
		*total++
		*final++
	} else if newPos >= numDials {
		newPos -= numDials
		*total++
		if newPos == 0 {
			*final++
		}
	}

	return newPos
}

func parseLine(line string) (dir int, steps int) {
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
	if steps <= 0 {
		panic(fmt.Sprintf("zero number of steps in line '%q'", line))
	}
	return
}

func CountZeroes(lines []string) (final int, total int) {
	pos := 50
	for _, line := range lines {
		dir, steps := parseLine(line)
		pos = updatePos(pos, dir, steps, &final, &total)
	}
	return
}
