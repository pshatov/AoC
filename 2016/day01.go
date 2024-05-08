package day01

import (
	"math"
	"strconv"
	"strings"
)

const (
	N = iota
	E
	S
	W
	NUM_DIRS
)

type XY struct {
	X, Y int
}

func turn(dir int, prefix rune) int {
	switch prefix {
	case 'L':
		dir -= 1
	case 'R':
		dir += 1
	default:
		panic("bad prefix!")
	}
	if dir < 0 {
		dir += NUM_DIRS
	} else if dir >= NUM_DIRS {
		dir -= NUM_DIRS
	}
	return dir
}

func move(xy XY, dir int, count int) XY {
	switch dir {
	case N:
		xy.Y += count
	case E:
		xy.X += count
	case S:
		xy.Y -= count
	case W:
		xy.X -= count
	default:
		panic("bad dir!")
	}
	return xy
}

func (xy *XY) Dist() int {
	return int(math.Abs(float64(xy.X)) + math.Abs(float64(xy.Y)))
}

func Part1(doc string) (int, []XY) {

	docNoCommas := strings.ReplaceAll(doc, ",", "")
	docParts := strings.Fields(docNoCommas)

	route := []XY{{0, 0}}

	dir, xy := N, XY{}
	for _, p := range docParts {

		r := []rune(p)
		if n := len(r); n < 2 {
			panic("p is too short!")
		}

		prefix := r[0]
		count, err := strconv.Atoi(string(r[1:]))
		if err != nil {
			panic("bad count string!")
		}
		dir = turn(dir, prefix)
		xy_new := move(xy, dir, count)
		dx, dy := 0, 0
		switch {
		case xy_new.X > xy.X:
			dx = 1
		case xy_new.X < xy.X:
			dx = -1
		}
		switch {
		case xy_new.Y > xy.Y:
			dy = 1
		case xy_new.Y < xy.Y:
			dy = -1
		}
		for i := 0; i < count; i++ {
			xy.X, xy.Y = xy.X+dx, xy.Y+dy
			route = append(route, xy)
		}
	}
	return xy.Dist(), route
}

func Part2(route []XY) int {
	for i, xy := range route {
		for j := 0; j < i; j++ {
			if xy == route[j] {
				return xy.Dist()
			}
		}
	}
	panic("bad route!")
}
