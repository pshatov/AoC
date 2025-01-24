package day02

import (
	"fmt"
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestGetSign(t *testing.T) {
	for _, tc := range []struct {
		level int
		sign  int
	}{
		{-10, -1},
		{-1, -1},
		{0, 1},
		{1, 1},
		{10, 1},
	} {
		s := getSign(tc.level)
		assert.Equal(t, tc.sign, s)
	}
}

func TestSafetyCheckers(t *testing.T) {
	testCases := []struct {
		levels                 []int
		isSafe, isSafeDampened bool
	}{
		{[]int{7, 6, 4, 2, 1}, true, true},
		{[]int{1, 2, 7, 8, 9}, false, false},
		{[]int{9, 7, 6, 2, 1}, false, false},
		{[]int{1, 3, 2, 4, 5}, false, true},
		{[]int{8, 6, 4, 4, 1}, false, true},
		{[]int{1, 3, 6, 7, 9}, true, true},
	}
	for i, tc := range testCases {
		r := Report(tc.levels)
		t.Run(
			fmt.Sprintf("Test_isSafe_%d_of_%d", i+1, len(testCases)),
			func(t *testing.T) {
				ok := r.isSafe()
				assert.Equal(t, tc.isSafe, ok)
			})
		t.Run(
			fmt.Sprintf("Test_isSafeDampened_%d_of_%d", i+1, len(testCases)),
			func(t *testing.T) {
				ok := r.isSafeDampened()
				assert.Equal(t, tc.isSafeDampened, ok)
			})
	}
}
