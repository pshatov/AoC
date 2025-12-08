package day04

import (
	"aoc/2025/util"
)

const (
	DayNN      = "day04"
	IntEmpty   = 0
	IntRoll    = 1
	IntRemoved = 2
)

var MazeKey = map[byte]int{
	'.': IntEmpty,
	'@': IntRoll,
	'X': IntRemoved,
}

func GetAccessibleRolls(maze *util.Maze) []util.XY {
	addedBorder := false
	if !maze.HasBorder() {
		maze.AddBorder(IntEmpty)
		addedBorder = true
	}
	points := []util.XY{}
	for y0 := 1; y0 < maze.Dy()-1; y0++ {
		for x0 := 1; x0 < maze.Dx()-1; x0++ {
			if maze.At(y0, x0) != IntRoll {
				continue
			}
			s := -1
			for dy := -1; dy <= 1; dy++ {
				for dx := -1; dx <= 1; dx++ {
					y, x := y0+dy, x0+dx
					if maze.At(y, x) == IntRoll {
						s++
					}
				}
			}
			if s < 4 {
				points = append(points, util.XY{X: x0, Y: y0})
			}
		}
	}
	if addedBorder {
		maze.RemoveBorder()
	}
	return points
}

func RemoveAccessibleRolls(maze *util.Maze) int {
	total := 0
	addedBorder := false
	if !maze.HasBorder() {
		maze.AddBorder(IntEmpty)
		addedBorder = true
	}
	for {
		points := GetAccessibleRolls(maze)
		if len(points) == 0 {
			break
		}
		total += len(points)
		for _, p := range points {
			maze.Set(p.Y, p.X, IntRemoved)
		}
	}
	if addedBorder {
		maze.RemoveBorder()
	}
	return total
}
