package day05_test

import (
	"pshatov/aoc/year2016/day05"
	"pshatov/aoc/year2016/day05/vectors"
	"testing"
)

// TODO: Add unit test to check that finding 00000-prefix hashes works

func TestPart1(t *testing.T) {
	for _, c := range vectors.CasesPart1 {
		got := day05.Part1(c.In, true)
		if got != c.Want {
			t.Errorf("Part1(%#v) == %#v, want %#v", c.In, got, c.Want)
		}
	}
}

func TestPart2(t *testing.T) {
	for _, c := range vectors.CasesPart2 {
		got := day05.Part2(c.In, true)
		if got != c.Want {
			t.Errorf("Part2(%#v) == %#v, want %#v", c.In, got, c.Want)
		}
	}
}
