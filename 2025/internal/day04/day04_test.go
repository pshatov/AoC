package day04

import (
	"aoc/2025/util"
	"testing"
)

func TestCalcAccessibleRolls(t *testing.T) {
	example := util.NewMaze(util.ReadAllLines("example.txt"), MazeKey)
	input := util.NewMaze(util.ReadAllLines("input.txt"), MazeKey)

	tests := []struct {
		title                  string
		maze                   *util.Maze
		wantsPart1, wantsPart2 int
	}{
		{"example", &example, 13, 43},
		{"input", &input, 1320, 8354},
	}

	for _, tc := range tests {
		t.Run(tc.title, func(t *testing.T) {
			points := GetAccessibleRolls(tc.maze)
			num := len(points)
			if num != tc.wantsPart1 {
				t.Fatalf("CalcAccessibleRolls(%s) result = %d, but wants = %d", tc.title, num, tc.wantsPart1)
			}
			num = RemoveAccessibleRolls(tc.maze)
			if num != tc.wantsPart2 {
				t.Fatalf("RemoveAccessibleRolls(%s) result = %d, but wants = %d", tc.title, num, tc.wantsPart2)
			}
		})
	}
}
