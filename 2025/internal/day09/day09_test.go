package day09

import (
	"aoc/2025/util"
	"testing"
)

type testData struct {
	title string
	tiles []util.XY
}

var (
	exampleData = testData{
		title: "example",
		tiles: parseLines(util.ReadAllLines("example.txt")),
	}
	inputData = testData{
		title: "input",
		tiles: parseLines(util.ReadAllLines("input.txt")),
	}
)

func TestLargestRectangle(t *testing.T) {
	tests := []struct {
		data      testData
		wantsArea int
	}{
		{exampleData, 50},
		{inputData, 4758121828},
	}

	for _, tc := range tests {
		t.Run("FindLargestRectangle_"+tc.data.title, func(t *testing.T) {
			area := FindLargestRectangle(tc.data.tiles)
			if area != tc.wantsArea {
				t.Fatalf(
					"FindLargestRectangle(%s) result = %d, but tc.wantsArea = %d",
					tc.data.title, area, tc.wantsArea)
			}
		})
	}
}
