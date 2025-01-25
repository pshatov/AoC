package day02_test

import (
	"fmt"
	"pshatov/aoc/year2024/day02"
	"pshatov/aoc/year2024/util"
	"strconv"
	"strings"
	"testing"

	"github.com/stretchr/testify/assert"
)

func parseData(lines []string) (reports []day02.Report) {
	for _, ln := range lines {
		r := day02.Report{}
		fields := strings.Fields(ln)
		for _, val := range fields {
			num, err := strconv.Atoi(val)
			if err != nil {
				panic(fmt.Errorf("can't parse input line '%s': bad field '%s'", ln, val))
			}
			r = append(r, num)
		}
		reports = append(reports, r)
	}
	return
}

func TestNumSafeCalculators(t *testing.T) {
	for _, tc := range []struct {
		data                     string
		numSafe, numSafeDampened int
	}{
		{"example", 2, 4},
		{"input", 230, 301},
	} {
		lines := util.LoadData("..", day02.Day, tc.data)
		reports := parseData(lines)
		t.Run(
			fmt.Sprintf("CalcNumSafe_%s", tc.data),
			func(t *testing.T) {
				n := day02.CalcNumSafe(reports)
				assert.Equal(t, tc.numSafe, n)
			})
		t.Run(
			fmt.Sprintf("CalcNumSafeDampened_%s", tc.data),
			func(t *testing.T) {
				n := day02.CalcNumSafeDampened(reports)
				assert.Equal(t, tc.numSafeDampened, n)
			})
	}
}
