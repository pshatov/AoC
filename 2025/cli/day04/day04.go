package main

import (
	"aoc/2025/internal/day04"
	"aoc/2025/util"
	"fmt"
	"os"
)

func main() {
	if len(os.Args) != 2 {
		fmt.Printf("USAGE: %s <file>\n", day04.DayNN)
		os.Exit(1)
	}
	file := fmt.Sprintf("%s/%s/%s.txt", "../../internal", day04.DayNN, os.Args[1])
	fmt.Printf("Using maze file '%s'\n", file)
	lines := util.ReadAllLines(file)
	maze := util.NewMaze(lines, day04.MazeKey)
	fmt.Printf("Maze is %d rows x %d cols\n", maze.Dy(), maze.Dx())
	_ = day04.RemoveAccessibleRolls(&maze)
	maze.DebugPrint()
	os.Exit(0)
}
