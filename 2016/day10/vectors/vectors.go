package vectors

import (
	"pshatov/aoc/year2016/day10"
	"pshatov/aoc/year2016/util"
	"testing"
)

type VectorInline struct {
	In     []string
	Target [2]int
	Want   int
}

type VectorFile struct {
	Target [2]int
	Want   int
}

func (v *VectorFile) ToInline(t *testing.T) VectorInline {
	path := util.FormatDataPath(day10.DayNumber)
	lines := util.LoadDataStrings(t, path)
	return VectorInline{lines, v.Target, v.Want}
}

var (
	Example = VectorInline{
		[]string{
			"value 5 goes to bot 2",
			"bot 2 gives low to bot 1 and high to bot 0",
			"value 3 goes to bot 1",
			"bot 1 gives low to output 1 and high to bot 0",
			"bot 0 gives low to output 2 and high to output 0",
			"value 2 goes to bot 2",
		}, [2]int{2, 5}, 2}

	Input = VectorFile{[2]int{61, 17}, 161}
)
