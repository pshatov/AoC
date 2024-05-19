package day07_test

import (
	"fmt"
	"pshatov/aoc/year2016/day07"
	"pshatov/aoc/year2016/day07/vectors"
	"pshatov/aoc/year2016/util"
	"testing"
)

func testHasBackdoor(
	t *testing.T,
	title string,
	cases []vectors.TestCaseHasBackdoor,
	f func(string) bool) {
	for _, c := range cases {
		got := f(c.In)
		if got != c.Want {
			t.Errorf("Has%#v(%#v) == %#v, want %#v", title, c.In, got, c.Want)
		}
	}
}

func TestHasTLS(t *testing.T) {
	testHasBackdoor(t, "TLS", vectors.CasesHasTLS, day07.HasTLS)
}

func TestHasSSL(t *testing.T) {
	testHasBackdoor(t, "SSL", vectors.CasesHasSSL, day07.HasSSL)
}

func testPart(t *testing.T, part int, f func([]string) int) {
	cases, ok := vectors.CasesPart[part]
	if !ok {
		t.Logf("No cases for part %v", part)
		t.FailNow()
	}
	for _, c := range cases {
		fn := fmt.Sprintf("../data/day%02v_%v.txt", day07.DayNumber, c.Title)
		in := util.LoadDataStrings(t, fn)
		got := f(in)
		if got != c.Want {
			t.Errorf("Part%v(%#v) == %#v, want %#v", part, c.Title, got, c.Want)
		}
	}
}

func TestPart1(t *testing.T) {
	testPart(t, 1, day07.Part1)
}

func TestPart2(t *testing.T) {
	testPart(t, 2, day07.Part2)
}
