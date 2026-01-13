package day09

import (
	"aoc/2025/util"
	"fmt"
	"strconv"
	"strings"
)

func absInt(x int) int {
	if x < 0 {
		x = -x
	}
	return x
}

func parseLines(lines []string) []util.XY {
	result := []util.XY{}
	for _, ln := range lines {
		parts := strings.Split(ln, ",")
		if n := len(parts); n != 2 {
			panic(fmt.Errorf("bad line '%s', expected 2 parts, but has %d", ln, n))
		}
		x, err := strconv.Atoi(parts[0])
		if err != nil {
			panic(fmt.Errorf("bad x part in line '%s'", ln))
		}
		y, err := strconv.Atoi(parts[1])
		if err != nil {
			panic(fmt.Errorf("bad y part in line '%s'", ln))
		}
		result = append(result, util.XY{X: x, Y: y})
	}
	return result
}

func FindLargestRectangle(tiles []util.XY) int {
	n := len(tiles)
	maxArea := 0
	for i := 0; i < n-1; i++ {
		for j := i + 1; j < n; j++ {
			dx := absInt(tiles[i].X - tiles[j].X)
			dy := absInt(tiles[i].Y - tiles[j].Y)
			area := (dx + 1) * (dy + 1)
			if area > maxArea {
				maxArea = area
			}
		}
	}
	return maxArea
}
