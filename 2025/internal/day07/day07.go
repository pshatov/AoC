package day07

import (
	"aoc/2025/util"
)

func linesToBytes(lines []string) (dx, dy int, field [][]byte) {
	dy = len(lines)
	dx = len(lines[dy-1])
	field = make([][]byte, dy)
	for y := range dy {
		field[y] = []byte(lines[y])
	}
	return
}

func CalcNumSplits(lines []string) int {
	dx, dy, field := linesToBytes(lines)
	total := 0
	for y := range dy - 1 {
		for x := range dx {
			if y == 0 && field[y][x] == 'S' {
				field[y+1][x] = '|'
			}
			if y > 0 && field[y][x] == '|' {
				switch field[y+1][x] {
				case '.', '|':
					field[y+1][x] = '|'
				case '^':
					if x == 0 || x == dx-1 {
						panic("bad field")
					}
					total += 1
					field[y+1][x-1] = '|'
					field[y+1][x+1] = '|'
				}
			}
		}
	}
	return total
}

func advanceTimelines(dx, dy int, xy util.XY, field [][]byte, subtotal int, cache map[util.XY]int) int {
	if xy.Y == dy-1 {
		return subtotal + 1
	}

	xyDown := util.XY{X: xy.X, Y: xy.Y + 1}
	xyDownLeft := util.XY{X: xyDown.X - 1, Y: xyDown.Y}
	xyDownRight := util.XY{X: xyDown.X + 1, Y: xyDown.Y}

	if field[xy.Y+1][xy.X] != '^' {
		return advanceTimelines(dx, dy, xyDown, field, subtotal, cache)
	}

	total, ok := cache[xy]
	if ok {
		return total
	}
	left := advanceTimelines(dx, dy, xyDownLeft, field, subtotal, cache)
	right := advanceTimelines(dx, dy, xyDownRight, field, subtotal, cache)
	total = left + right
	cache[xy] = total
	return total

}

func CalcNumTimelines(lines []string) int {
	dx, dy, field := linesToBytes(lines)
	x0 := -1
	for x := range dx {
		if field[0][x] == 'S' {
			if x0 >= 0 {
				panic("more than one starting point")
			}
			x0 = x
		}
	}
	if x0 < 0 {
		panic("no starting point")
	}
	cache := make(map[util.XY]int, 0)
	return advanceTimelines(dx, dy, util.XY{X: x0, Y: 0}, field, 0, cache)
}
