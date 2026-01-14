package util

type XY struct {
	X, Y int
}

type XYZ struct {
	X, Y, Z int
}

type Dir int

const (
	_ Dir = iota
	Left
	Right
	Up
	Down
)

type Pos int

const (
	_ Pos = iota
	Above
	Below
	ToLeft
	ToRight
)

type LineXY struct {
	Begin, End XY
}

// TODO: write unit tests
func (l LineXY) IsVertical() bool {
	return l.Begin.X == l.End.X
}

// TODO: write unit tests
func (l LineXY) IsHorizontal() bool {
	return l.Begin.Y == l.End.Y
}

// TODO: write unit tests
func (l LineXY) GetDir() Dir {
	if l.IsVertical() {
		if l.Begin.Y < l.End.Y {
			return Up
		}
		if l.Begin.Y > l.End.Y {
			return Down
		}
	}
	if l.IsHorizontal() {
		if l.Begin.X < l.End.X {
			return Right
		}
		if l.Begin.X > l.End.X {
			return Left
		}
	}
	panic("line is neither vertical nor horizontal")
}
