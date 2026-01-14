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

func TestGetOuterLines(t *testing.T) {
	innerLines := []util.LineXY{
		{Begin: util.XY{X: -5, Y: -5}, End: util.XY{X: -10, Y: -5}},
		{Begin: util.XY{X: -10, Y: -5}, End: util.XY{X: -10, Y: 5}},
		{Begin: util.XY{X: -10, Y: 5}, End: util.XY{X: -5, Y: 5}},

		{Begin: util.XY{X: -5, Y: 5}, End: util.XY{X: -5, Y: 10}},
		{Begin: util.XY{X: -5, Y: 10}, End: util.XY{X: 5, Y: 10}},
		{Begin: util.XY{X: 5, Y: 10}, End: util.XY{X: 5, Y: 5}},

		{Begin: util.XY{X: 5, Y: 5}, End: util.XY{X: 10, Y: 5}},
		{Begin: util.XY{X: 10, Y: 5}, End: util.XY{X: 10, Y: -5}},
		{Begin: util.XY{X: 10, Y: -5}, End: util.XY{X: 5, Y: -5}},

		{Begin: util.XY{X: 5, Y: -5}, End: util.XY{X: 5, Y: -10}},
		{Begin: util.XY{X: 5, Y: -10}, End: util.XY{X: -5, Y: -10}},
		{Begin: util.XY{X: -5, Y: -10}, End: util.XY{X: -5, Y: -5}},
	}
	want := []util.LineXY{
		{Begin: util.XY{X: -6, Y: -6}, End: util.XY{X: -11, Y: -6}},
		{Begin: util.XY{X: -11, Y: -6}, End: util.XY{X: -11, Y: 6}},
		{Begin: util.XY{X: -11, Y: 6}, End: util.XY{X: -6, Y: 6}},

		{Begin: util.XY{X: -6, Y: 6}, End: util.XY{X: -6, Y: 11}},
		{Begin: util.XY{X: -6, Y: 11}, End: util.XY{X: 6, Y: 11}},
		{Begin: util.XY{X: 6, Y: 11}, End: util.XY{X: 6, Y: 6}},

		{Begin: util.XY{X: 6, Y: 6}, End: util.XY{X: 11, Y: 6}},
		{Begin: util.XY{X: 11, Y: 6}, End: util.XY{X: 11, Y: -6}},
		{Begin: util.XY{X: 11, Y: -6}, End: util.XY{X: 6, Y: -6}},

		{Begin: util.XY{X: 6, Y: -6}, End: util.XY{X: 6, Y: -11}},
		{Begin: util.XY{X: 6, Y: -11}, End: util.XY{X: -6, Y: -11}},
		{Begin: util.XY{X: -6, Y: -11}, End: util.XY{X: -6, Y: -6}},
	}
	validateLines(innerLines)
	validateLines(want)
	result := getOuterLines(innerLines)
	if len(result) != len(want) {
		t.Fatalf("len(result) = %d, but len(want) = %d",
			len(result), len(want))
	}
	for i := range result {
		if result[i] != want[i] {
			t.Fatalf("result[%d] = %v, but want[%d] = %v",
				i, result[i], i, want[i])
		}
	}
}

func TestFindLargestRectangle(t *testing.T) {
	tests := []struct {
		data                           testData
		wantsAreaPart1, wantsAreaPart2 int
	}{
		{exampleData, 50, 24},
		{inputData, 4758121828, 1577956170},
	}

	for _, tc := range tests {
		t.Run("part1_"+tc.data.title, func(t *testing.T) {
			area := FindLargestRectanglePart1(tc.data.tiles)
			if area != tc.wantsAreaPart1 {
				t.Fatalf("result = %d, but wants = %d", area, tc.wantsAreaPart1)
			}
		})
		t.Run("part2_"+tc.data.title, func(t *testing.T) {
			area := FindLargestRectanglePart2(tc.data.tiles)
			if area != tc.wantsAreaPart2 {
				t.Fatalf("result = %d, but wants = %d", area, tc.wantsAreaPart2)
			}
		})
	}
}
