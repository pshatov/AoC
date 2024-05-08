package day01

import (
	"testing"
)

var (
	CasesPart1 = []struct {
		in   string
		want int
	}{
		{"R2, L3",
			5},
		{"R2, R2, R2",
			2},
		{"R5, L5, R5, R3",
			12},
		{"R4, R4, L1, R3, L5, R2, R5, R1, L4, R3, L5, R2, L3, L4, L3, R1, R5, R1, L3, L1, R3, L1, R2, R2, L2, R5, L3, L4, R4, R4, R2, L4, L1, R5, L1, L4, R4, L1, R1, L2, R5, L2, L3, R2, R1, L194, R2, L4, R49, R1, R3, L5, L4, L1, R4, R2, R1, L5, R3, L5, L4, R4, R4, L2, L3, R78, L5, R4, R191, R4, R3, R1, L2, R1, R3, L1, R3, R4, R2, L2, R1, R4, L5, R2, L2, L4, L2, R1, R2, L3, R5, R2, L3, L3, R3, L1, L1, R5, L4, L4, L2, R5, R1, R4, L3, L5, L4, R5, L4, R5, R4, L3, L2, L5, R4, R3, L3, R1, L5, R5, R1, L3, R2, L5, R5, L3, R1, R4, L5, R4, R2, R3, L4, L5, R3, R4, L5, L5, R4, L4, L4, R1, R5, R3, L1, L4, L3, L4, R1, L5, L1, R2, R2, R4, R4, L5, R4, R1, L1, L1, L3, L5, L2, R4, L3, L5, L4, L1, R3",
			146},
	}
)

var (
	CasesPart2 = []struct {
		in   string
		want int
	}{
		{"R8, R4, R4, R8",
			4},
		{CasesPart1[len(CasesPart1)-1].in,
			131},
	}
)

func TestPart1(t *testing.T) {
	for _, c := range CasesPart1 {
		got, _ := Part1(c.in)
		if got != c.want {
			t.Errorf("Part1(%#v) == %#v, want %#v", c.in, got, c.want)
		}
	}
}

func TestPart2(t *testing.T) {
	for _, c := range CasesPart2 {
		_, route := Part1(c.in)
		got := Part2(route)
		if got != c.want {
			t.Errorf("Part2(%#v) == %#v, want %#v", c.in, got, c.want)
		}
	}
}
