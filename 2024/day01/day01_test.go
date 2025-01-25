package day01_test

import (
	"fmt"
	"pshatov/aoc/year2024/day01"
	"pshatov/aoc/year2024/util"
	"strconv"
	"strings"
	"testing"

	"github.com/stretchr/testify/assert"
)

func parseData(lines []string) (a, b []int) {
	for _, ln := range lines {
		fields := strings.Fields(ln)
		for idx, val := range fields {
			num, err := strconv.Atoi(val)
			if err != nil {
				panic(fmt.Errorf("can't parse input line '%s': bad field '%s'", ln, val))
			}
			var t *[]int
			switch idx {
			case 0:
				t = &a
			case 1:
				t = &b
			default:
				panic(fmt.Errorf("can't parse input line '%s': encountered more than two fields", ln))
			}
			*t = append(*t, num)
		}
	}
	return
}

func TestDistanceAndSimilarity(t *testing.T) {
	for _, tc := range []struct {
		data                 string
		distance, similarity int
	}{
		{"example", 11, 31},
		{"input", 3569916, 26407426},
	} {
		lines := util.LoadData("..", day01.Day, tc.data)
		a, b := parseData(lines)
		t.Run(
			fmt.Sprintf("distance_%s", tc.data),
			func(t *testing.T) {
				c := day01.ComputeDistance(a, b)
				assert.Equal(t, tc.distance, c)
			})
		t.Run(
			fmt.Sprintf("similarity_%s", tc.data),
			func(t *testing.T) {
				c := day01.ComputeSimilarity(a, b)
				assert.Equal(t, tc.similarity, c)
			})
	}
}
