package day02

import (
	"errors"
)

const Day = 2

type Report []int

var ErrBadReport = errors.New("bad report: too short, must have at least two levels")

func getSign(v int) int {
	if v < 0 {
		return -1
	}
	return 1
}

func (r Report) isSafe() bool {
	if len(r) < 2 {
		panic(ErrBadReport)
	}
	previousSign := 0
	for i := 1; i < len(r); i++ {
		delta := r[i] - r[i-1]
		if delta == 0 || delta < -3 || delta > 3 {
			return false
		}
		currentSign := getSign(delta)
		if previousSign != 0 && currentSign != previousSign {
			return false
		}
		previousSign = currentSign
	}
	return true
}

func (r Report) isSafeDampened() bool {
	if r.isSafe() {
		return true
	}
	for i := 0; i < len(r); i++ {
		part := make([]int, 0, len(r)-1)
		part = append(part, r[:i]...)
		part = append(part, r[i+1:]...)
		tmp := Report(part)
		if tmp.isSafe() {
			return true
		}
	}
	return false
}

func CalcNumSafe(reports []Report) int {
	total := 0
	for _, r := range reports {
		if r.isSafe() {
			total++
		}
	}
	return total
}

func CalcNumSafeDampened(reports []Report) int {
	total := 0
	for _, r := range reports {
		if r.isSafeDampened() {
			total++
		}
	}
	return total
}
