package day04

import (
	"aoc/2025/util"
)

const (
	DayNN    = "day04"
	IntEmpty = 0
	IntRoll  = 1
)

var MazeKey = map[byte]int{
	'.': IntEmpty,
	'@': IntRoll,
}

func CalcAccessibleRolls(lines []string) int {
	maze := util.NewMaze(lines, MazeKey)
	maze.AddBorder(IntEmpty)
	total := 0
	for y := 1; y < maze.Dy()-1; y++ {
		for x := 1; x < maze.Dx()-1; x++ {
			if maze.At(y, x) != IntRoll {
				continue
			}
			s := -1
			for dy := -1; dy <= 1; dy++ {
				for dx := -1; dx <= 1; dx++ {
					if maze.At(y+dy, x+dx) == IntRoll {
						s++
					}
				}
			}
			if s < 4 {
				total++
			}
		}
	}

	return total
}
