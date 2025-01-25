package day04_test

import (
	"fmt"
	"pshatov/aoc/year2024/day04"
	"pshatov/aoc/year2024/util"
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestFinder(t *testing.T) {
	for _, tc := range []struct {
		data               string
		numberV1, numberV2 int
	}{
		{"example", 18, 9},
		{"input", 2569, 1998},
	} {
		lines := util.LoadData("..", day04.Day, tc.data)
		t.Run(
			fmt.Sprintf("TestFindXMASv1_%s", tc.data),
			func(t *testing.T) {
				n, _ := day04.FindXMASv1(lines)
				assert.Equal(t, tc.numberV1, n)
			})
		t.Run(
			fmt.Sprintf("TestFindXMASv2_%s", tc.data),
			func(t *testing.T) {
				n, _ := day04.FindXMASv2(lines)
				assert.Equal(t, tc.numberV2, n)
			})
	}
}
