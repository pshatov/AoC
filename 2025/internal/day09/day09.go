package day09

import (
	"aoc/2025/util"
	"fmt"
	"strconv"
	"strings"
)

func tilesToLines(tiles []util.XY) []util.LineXY {
	n := len(tiles)
	lines := make([]util.LineXY, n)
	for j := range n {
		i := j - 1
		if i == -1 {
			i = n - 1
		}
		lines[i] = util.LineXY{Begin: tiles[i], End: tiles[j]}
	}
	return lines
}

func validateLines(lines []util.LineXY) {
	n := len(lines)
	for j, mid := range lines {
		if mid.Begin.X == mid.End.X {
			if h := util.AbsInt(mid.Begin.Y - mid.End.Y); h < 2 {
				panic("width too small")
			}
		} else if mid.Begin.Y == mid.End.Y {
			if w := util.AbsInt(mid.Begin.X - mid.End.X); w < 2 {
				panic("height too small")
			}
		} else {
			panic("line is neither horizontal nor vertical")
		}

		i, k := j-1, j+1
		if i == -1 {
			i = n - 1
		}
		if k == n {
			k = 0
		}
		left, right := lines[i], lines[k]
		if left.End != mid.Begin {
			panic("left and mid don't touch")
		}
		if mid.End != right.Begin {
			panic("mid and right don't touch")
		}
	}
}

func getMaxY(lines []util.LineXY) int {
	maxY := -1
	for _, l := range lines {
		if l.Begin.Y != l.End.Y {
			continue
		}
		if maxY < 0 {
			maxY = l.Begin.Y
			continue
		}
		maxY = util.MaxInt(maxY, l.Begin.Y)
	}
	return maxY
}

func getStartingIndex(lines []util.LineXY, minY int) int {
	for j, l := range lines {
		if l.Begin.Y != l.End.Y {
			continue
		}
		if l.Begin.Y == minY {
			return j
		}
	}
	panic("no starting line")
}

func incIndex(current, length int) int {
	next := current + 1
	if next == length {
		next = 0
	}
	return next
}

func getOuterEndPos(curPos util.Pos, curInnerLine util.LineXY, nextDir util.Dir) (curOuterEnd util.XY, nextPos util.Pos) {
	turnRightLUT := map[util.Dir]map[util.Dir]bool{
		util.Right: {util.Down: true},
		util.Down:  {util.Left: true},
		util.Left:  {util.Up: true},
		util.Up:    {util.Right: true},
	}
	turnLeftLUT := map[util.Dir]map[util.Dir]bool{
		util.Left:  {util.Down: true},
		util.Down:  {util.Right: true},
		util.Right: {util.Up: true},
		util.Up:    {util.Left: true},
	}
	turnRight := turnRightLUT[curInnerLine.GetDir()][nextDir]
	turnLeft := turnLeftLUT[curInnerLine.GetDir()][nextDir]

	if turnRight && turnLeft {
		panic("internal error, both turns")
	}
	if !turnRight && !turnLeft {
		panic("internal error, no turns")
	}

	nextPosLUT := map[util.Pos]map[bool]util.Pos{
		util.Above: {
			true:  util.ToRight,
			false: util.ToLeft,
		},
		util.Below: {
			true:  util.ToLeft,
			false: util.ToRight,
		},
		util.ToLeft: {
			true:  util.Above,
			false: util.Below,
		},
		util.ToRight: {
			true:  util.Below,
			false: util.Above,
		},
	}
	nextPos = nextPosLUT[curPos][turnRight]

	curOuterEnd = curInnerLine.End
	switch curPos {
	case util.Above:
		curOuterEnd.Y++
	case util.Below:
		curOuterEnd.Y--
	case util.ToLeft:
		curOuterEnd.X--
	case util.ToRight:
		curOuterEnd.X++
	}

	dLUT := map[bool]int{
		true:  1,
		false: -1,
	}

	dx, dy := 0, 0
	switch curInnerLine.GetDir() {
	case util.Left, util.Right:
		switch curPos {
		case util.Above:
			dx = dLUT[turnRight]
		case util.Below:
			dx = -dLUT[turnRight]
		}
	case util.Up, util.Down:
		switch curPos {
		case util.ToLeft:
			dy = dLUT[turnRight]
		case util.ToRight:
			dy = -dLUT[turnRight]
		}
	}
	if dx == 0 && dy == 0 {
		panic("internal error")
	}
	curOuterEnd.X += dx
	curOuterEnd.Y += dy
	return
}

func getOuterLines(lines []util.LineXY) []util.LineXY {
	n := len(lines)
	maxY := getMaxY(lines)
	curIndex := getStartingIndex(lines, maxY)

	curPos := util.Above
	curOuterBegin := lines[curIndex].Begin
	curOuterBegin.Y++
	if d := lines[curIndex].GetDir(); d == util.Right {
		curOuterBegin.X--
	} else if d == util.Left {
		curOuterBegin.X++
	} else {
		panic("internal error")
	}

	result := make([]util.LineXY, n)
	for range n {
		nextIndex := incIndex(curIndex, n)
		curInnerLine, nextInnerLine := lines[curIndex], lines[nextIndex]
		nextDir := nextInnerLine.GetDir()
		curOuterEnd, nextPos := getOuterEndPos(curPos, curInnerLine, nextDir)
		curOuterLine := util.LineXY{Begin: curOuterBegin, End: curOuterEnd}
		result[curIndex] = curOuterLine
		curPos, curIndex = nextPos, nextIndex
		curOuterBegin = curOuterEnd
	}
	return result
}

func parseLines(lines []string) []util.XY {
	result := []util.XY{}
	for _, ln := range lines {
		parts := strings.Split(ln, ",")
		if n := len(parts); n != 2 {
			panic(fmt.Errorf("bad line '%s', expected 2 parts, but has %d", ln, n))
		}
		x, err := strconv.Atoi(parts[0])
		if err != nil {
			panic(fmt.Errorf("bad x part in line '%s'", ln))
		}
		y, err := strconv.Atoi(parts[1])
		if err != nil {
			panic(fmt.Errorf("bad y part in line '%s'", ln))
		}
		result = append(result, util.XY{X: x, Y: y})
	}
	return result
}

func FindLargestRectanglePart1(tiles []util.XY) int {
	n := len(tiles)
	maxArea := 0
	for i := 0; i < n-1; i++ {
		for j := i + 1; j < n; j++ {
			dx := util.AbsInt(tiles[i].X - tiles[j].X)
			dy := util.AbsInt(tiles[i].Y - tiles[j].Y)
			area := (dx + 1) * (dy + 1)
			if area > maxArea {
				maxArea = area
			}
		}
	}
	return maxArea
}

func FindLargestRectanglePart2(tiles []util.XY) int {
	innerLines := tilesToLines(tiles)
	validateLines(innerLines)

	outerLines := getOuterLines(innerLines)
	validateLines(outerLines)

	n := len(tiles)
	maxArea := 0
	for i := 0; i < n-1; i++ {
		for j := i + 1; j < n; j++ {
			ti, tj := tiles[i], tiles[j]
			tLeft, tRight := util.MinInt(ti.X, tj.X), util.MaxInt(ti.X, tj.X)
			tUp, tDown := util.MaxInt(ti.Y, tj.Y), util.MinInt(ti.Y, tj.Y)
			valid := true
			for _, l := range outerLines {
				if l.IsVertical() {
					lX := l.Begin.X
					if lX < tLeft || lX > tRight {
						continue
					}
					minY, maxY := util.MinInt(l.Begin.Y, l.End.Y), util.MaxInt(l.Begin.Y, l.End.Y)
					if minY > tUp || maxY < tDown {
						continue
					}
				}
				if l.IsHorizontal() {
					lY := l.Begin.Y
					if lY < tDown || lY > tUp {
						continue
					}
					minX, maxX := util.MinInt(l.Begin.X, l.End.X), util.MaxInt(l.Begin.X, l.End.X)
					if minX > tRight || maxX < tLeft {
						continue
					}
				}
				valid = false
			}
			if !valid {
				continue
			}

			dx := util.AbsInt(ti.X - tj.X)
			dy := util.AbsInt(ti.Y - tj.Y)
			area := (dx + 1) * (dy + 1)

			if area > maxArea {
				maxArea = area
			}
		}
	}

	return maxArea
}
