package util

func AbsInt(x int) int {
	if x < 0 {
		x = -x
	}
	return x
}

func MinInt(x, y int) int {
	if x < y {
		return x
	}
	return y
}

func MaxInt(x, y int) int {
	if x > y {
		return x
	}
	return y
}
