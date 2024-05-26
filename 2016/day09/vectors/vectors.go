package vectors

import (
	"pshatov/aoc/year2016/day09"
	"pshatov/aoc/year2016/util"
	"testing"
)

type VectorInline struct {
	In, Out string
	Want    int
}

type VectorFile struct {
	Size int
}

func (v *VectorFile) ToInline(t *testing.T) VectorInline {
	fn := util.FormatDataPath(day09.DayNumber)
	lines := util.LoadDataStrings(t, fn)
	if len(lines) != 1 {
		t.Logf("Can't read %v", fn)
		t.FailNow()
	}
	return VectorInline{lines[0], "", v.Size}
}

var (
	ExamplesV1 = []VectorInline{
		{"ADVENT", "ADVENT", 6},
		{"A(1x5)BC", "ABBBBBC", 7},
		{"(3x3)XYZ", "XYZXYZXYZ", 9},
		{"A(2x2)BCD(2x2)EFG", "ABCBCDEFEFG", 11},
		{"(6x1)(1x3)A", "(1x3)A", 6},
		{"X(8x2)(3x3)ABCY", "X(3x3)ABC(3x3)ABCY", 18},
	}

	InputV1 = VectorFile{107035}

	ExamplesV2 = []VectorInline{
		{"(3x3)XYZ", "XYZXYZXYZ", 0},
		{"X(8x2)(3x3)ABCY", "XABCABCABCABCABCABCY", 0},
		{"(27x12)(20x12)(13x14)(7x10)(1x12)A", "", 241920},
		{"(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN", "", 445},
	}

	InputV2 = VectorFile{11451628995}
)
