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
		result = updateResult(result, num, op)
	}
	return result
}

func updateResult(result int, num int, op string) int {
	switch op {
	case "+":
		return result + num
	case "*":
		return result * num
	}
	panic(fmt.Sprintf("update result failed, unknown op '%s'", op))
}

func calcColumnPart2(column []string) int {
	dy := len(column) - 1
	dx := len(column[dy])
	op := strings.TrimSpace(column[dy])
	var result int
	for x := dx - 1; x >= 0; x-- {
		tmp := []byte{}
		for y := range dy {
			tmp = append(tmp, column[y][x])
		}
		str := strings.TrimSpace(string(tmp))
		num, err := strconv.Atoi(str)
		if err != nil {
			panic(fmt.Sprintf("can't parse value '%s'", str))
		}
		if x == dx-1 {
			result = num
			continue
		}
		result = updateResult(result, num, op)
	}
	return result
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
