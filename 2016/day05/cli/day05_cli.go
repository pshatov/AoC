package main

import (
	"fmt"
	"pshatov/aoc/year2016/day05"
	"pshatov/aoc/year2016/day05/vectors"
)

func main() {
	fmt.Println("Part 1")
	fmt.Println("------")
	for _, c := range vectors.CasesPart1 {
		got := day05.Part1(c.In, false)
		if got != c.Want {
			panic("part1: got != want")
		}
		fmt.Println(" [OK]")
	}

	fmt.Println("Part 2")
	fmt.Println("------")
	for _, c := range vectors.CasesPart2 {
		got := day05.Part2(c.In, false)
		if got != c.Want {
			panic("part1: got != want")
		}
		fmt.Println(" [OK]")
	}
}
