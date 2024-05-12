package day04

import (
	"os"
	"strings"
	"testing"
)

type TestCaseVerifyChecksum struct {
	in   string
	want bool
}

type TestCaseDecryptRoom struct {
	in   string
	want string
}

type TestCase struct {
	in   string
	want int
}

var (
	CasesVerifyChecksum = []TestCaseVerifyChecksum{
		{"aaaaa-bbb-z-y-x-123[abxyz]",
			true},
		{"a-b-c-d-e-f-g-h-987[abcde]",
			true},
		{"not-a-real-room-404[oarel]",
			true},
		{"totally-real-room-200[decoy]",
			false},
	}
	CasesPart1 = []TestCase{
		{"../data/day04.txt",
			137896},
	}
	CasesDecryptRoom = []TestCaseDecryptRoom{
		{"qzmt-zixmtkozy-ivhz-343",
			"very encrypted name"},
	}
	CasesPart2 = []TestCase{
		{"../data/day04.txt",
			501},
	}
)

func LoadStrings(filename string, t *testing.T) []string {

	data, err := os.ReadFile(filename)
	if err != nil {
		t.Logf("Can't read %v", filename)
		t.FailNow()
	}

	allLines := strings.Split(string(data), "\n")
	filteredLines := []string{}
	for _, ln := range allLines {
		if t := len(ln); t > 0 {
			filteredLines = append(filteredLines, ln)
		}
	}

	// 254 too low
	return filteredLines
}

func TestVerifyChecksum(t *testing.T) {
	for _, c := range CasesVerifyChecksum {
		room := ParseRoom(c.in)
		got := room.IsValid()
		if got != c.want {
			t.Errorf("room.IsValid(%#v) == %#v, want %#v", c.in, got, c.want)
		}
	}
}

func TestPart1(t *testing.T) {
	for _, c := range CasesPart1 {
		in := LoadStrings(c.in, t)
		got := Part1(in)
		if got != c.want {
			t.Errorf("Part1(%#v) == %#v, want %#v", c.in, got, c.want)
		}
	}
}

func TestDecryptRoom(t *testing.T) {
	for _, c := range CasesDecryptRoom {
		name, sector := parseNameSector(c.in)
		room := Room{
			name:   name,
			sector: sector,
		}
		got := room.Decrypt()
		if got != c.want {
			t.Errorf("room.Decrypt(%#v) == %#v, want %#v", c.in, got, c.want)
		}
	}
}

func TestPart2(t *testing.T) {
	for _, c := range CasesPart2 {
		in := LoadStrings(c.in, t)
		got := Part2(in)
		if got != c.want {
			t.Errorf("Part2(%#v) == %#v, want %#v", c.in, got, c.want)
		}
	}
}
