package day06_test

import (
	"fmt"
	"pshatov/aoc/year2016/day06"
	"pshatov/aoc/year2016/day06/vectors"
	"pshatov/aoc/year2016/util"
	"testing"
)

func testFunc(t *testing.T, part int, f func([]string) string) {
	cases, ok := vectors.Cases[part]
	if !ok {
		t.Logf("No cases for part %v", part)
		t.FailNow()
	}
	for _, c := range cases {
		fn := fmt.Sprintf("../data/day%02v_%v.txt", day06.DayNumber, c.Title)
		in := util.LoadDataStrings(t, fn)
		got := f(in)
		if got != c.Want {
			t.Errorf("Part%v(%#v) == %#v, want %#v", part, c.Title, got, c.Want)
		}
	}
}

func TestPart1(t *testing.T) {
	testFunc(t, 1, day06.Part1)
}

func TestPart2(t *testing.T) {
	testFunc(t, 2, day06.Part2)
}
