package day06

import (
	"fmt"
	"strconv"
	"strings"
)

func splitColumns(lines []string) [][]string {
	dy := len(lines)
	dx := len(lines[dy-1])

	start := 0
	columns := make([][]string, 0)
	for x := range dx {
		emptyColumn := true
		for y := range dy {
			if lines[y][x] != ' ' {
				emptyColumn = false
				break
			}
		}
		if emptyColumn || x == dx-1 {
			stop := x
			if !emptyColumn && x == dx-1 {
				stop++
			}
			c := make([]string, dy)
			for y := range dy {
				c[y] = lines[y][start:stop]
			}
			columns = append(columns, c)
			start = x + 1
		}
	}

	return columns
}

func calcColumnPart1(column []string) int {
	dy := len(column) - 1
	op := strings.TrimSpace(column[dy])
	var result int
	for y := range dy {
		tmp := strings.TrimSpace(column[y])
		num, err := strconv.Atoi(tmp)
		if err != nil {
			panic(fmt.Sprintf("can't parse value '%s'", tmp))
		}
		if y == 0 {
			result = num
			continue
		}
		switch op {
		case "+":
			result += num
		case "*":
			result *= num
		}
	}
	return result
}

func calcColumnPart2(column []string) int {
	return len(column)
}

func CalcHomework(lines []string, rtl bool) int {
	columns := splitColumns(lines)
	total := 0
	for _, c := range columns {
		var delta int
		if !rtl {
			delta = calcColumnPart1(c)
		} else {
			delta = calcColumnPart2(c)
		}
		total += delta
	}
	return total
}
