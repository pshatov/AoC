package vectors

import (
	"fmt"
	"pshatov/aoc/year2016/day08"
	"pshatov/aoc/year2016/util"
	"testing"
)

type TestCaseInline struct {
	W, H    int
	In, Out []string
	Want    int
}

type TestCaseFile struct {
	W, H int
	In   string
	Out  []string
	Want int
}

func (tc *TestCaseFile) ToInline(t *testing.T) *TestCaseInline {
	seq := util.LoadDataStrings(t, tc.In)
	z := TestCaseInline{tc.W, tc.H, seq, tc.Out, tc.Want}
	return &z
}

var (
	CaseExample = TestCaseInline{
		W: 7,
		H: 3,
		In: []string{
			"rect 3x2",
			"rotate column x=1 by 1",
			"rotate row y=0 by 4",
			"rotate column x=1 by 1",
		},
		Out: []string{
			".#..#.#",
			"#.#....",
			".#.....",
		},
		Want: 6,
	}
	CaseInput = TestCaseFile{
		W:  50,
		H:  6,
		In: fmt.Sprintf("../data/day%02v.txt", day08.DayNumber),
		Out: []string{
			"####..##...##..###...##..###..#..#.#...#.##...##..",
			"#....#..#.#..#.#..#.#..#.#..#.#..#.#...##..#.#..#.",
			"###..#..#.#..#.#..#.#....#..#.####..#.#.#..#.#..#.",
			"#....#..#.####.###..#.##.###..#..#...#..####.#..#.",
			"#....#..#.#..#.#.#..#..#.#....#..#...#..#..#.#..#.",
			"####..##..#..#.#..#..###.#....#..#...#..#..#..##..",
		},
		Want: 128,
	}
)
