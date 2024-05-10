package day03

import (
	"os"
	"strconv"
	"strings"
	"testing"
)

type TestCaseIsValid struct {
	in   Triangle
	want bool
}

type TestCase struct {
	in   string
	want int
}

var (
	CasesIsValid = []TestCaseIsValid{
		{Triangle{5, 10, 25},
			false},
	}
	CasesPart1 = []TestCase{
		{"../data/day03.txt",
			1032},
	}
	CasesPart2 = []TestCase{
		{"../data/day03.txt",
			1838},
	}
)

func LoadTriangles(filename string, t *testing.T) []Triangle {

	data, err := os.ReadFile(filename)
	if err != nil {
		t.Logf("Can't read %v", filename)
		t.FailNow()
	}

	in := []Triangle{}
	lines := strings.Split(string(data), "\n")
	for _, ln := range lines {

		if n := len(ln); n == 0 {
			continue
		}

		fields := strings.Fields(ln)
		if n := len(fields); n != 3 {
			panic("length of fields is not 3!")
		}

		t1, err1 := strconv.Atoi(fields[0])
		t2, err2 := strconv.Atoi(fields[1])
		t3, err3 := strconv.Atoi(fields[2])
		if err1 != nil || err2 != nil || err3 != nil {
			panic("bad triangle!")
		}

		t := Triangle{t1, t2, t3}
		in = append(in, t)
	}

	return in
}

func TestIsValid(t *testing.T) {
	for _, c := range CasesIsValid {
		got := IsValid(&c.in)
		if got != c.want {
			t.Errorf("IsValid(%#v) == %#v, want %#v", c.in, got, c.want)
		}
	}
}

func TestPart1(t *testing.T) {
	for _, c := range CasesPart1 {
		in := LoadTriangles(c.in, t)
		got := Part1(in)
		if got != c.want {
			t.Errorf("Part1(%#v) == %#v, want %#v", c.in, got, c.want)
		}
	}
}

func TestPart2(t *testing.T) {
	for _, c := range CasesPart2 {
		in := LoadTriangles(c.in, t)
		got := Part2(in)
		if got != c.want {
			t.Errorf("Part1(%#v) == %#v, want %#v", c.in, got, c.want)
		}
	}
}
