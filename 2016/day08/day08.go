package day08

import (
	"strconv"
	"strings"
)

const (
	DayNumber = 8
)

type LCD struct {
	W, H int
	Dots []string
}

func MakeLCD(w, h int) *LCD {
	dots := make([]string, h)
	for y := 0; y < h; y++ {
		for x := 0; x < w; x++ {
			dots[y] += "."
		}
	}
	lcd := LCD{w, h, dots}
	return &lcd
}

func (lcd *LCD) CalcPwr() int {
	sum := 0
	for y := 0; y < lcd.H; y++ {
		for x := 0; x < lcd.W; x++ {
			if lcd.Dots[y][x] == '#' {
				sum++
			}
		}
	}
	return sum
}

func (lcd *LCD) Rect(a, b int) {
	for y := 0; y < b; y++ {
		for x := 0; x < a; x++ {
			lcd.Dots[y] = lcd.Dots[y][:x] + "#" + lcd.Dots[y][x+1:]
		}
	}
}

func (lcd *LCD) RotateRow(a, b int) {
	for n := 0; n < b; n++ {
		lcd.rotateRowOnce(a)
	}
}

func (lcd *LCD) RotateColumn(a, b int) {
	for n := 0; n < b; n++ {
		lcd.rotateColumnOnce(a)
	}
}

func (lcd *LCD) rotateRowOnce(a int) {
	t := lcd.Dots[a]
	n := len(t)
	lcd.Dots[a] = t[n-1:n] + t[:n-1]
}

func (lcd *LCD) rotateColumnOnce(a int) {
	n := len(lcd.Dots)
	t := lcd.Dots[n-1][a : a+1]
	for y := 0; y < n; y++ {
		s := lcd.Dots[y][a : a+1]
		lcd.Dots[y] = lcd.Dots[y][:a] + t + lcd.Dots[y][a+1:]
		t = s
	}
}

func tryPrefix(seq, prefix, sep string) (a, b int, ok bool) {
	s, found := strings.CutPrefix(seq, prefix)
	if !found {
		return
	}
	parts := strings.Split(s, sep)
	if len(parts) != 2 {
		panic("bad rect")
	}
	a, aErr := strconv.Atoi(parts[0])
	b, bErr := strconv.Atoi(parts[1])
	if aErr != nil {
		panic("rect a error")
	}
	if bErr != nil {
		panic("rect b error")
	}
	ok = true
	return
}

func Part(seq []string, lcd *LCD) int {

	for _, s := range seq {

		a, b, ok := tryPrefix(s, "rect ", "x")
		if ok {
			lcd.Rect(a, b)
			continue
		}

		a, b, ok = tryPrefix(s, "rotate row y=", " by ")
		if ok {
			lcd.RotateRow(a, b)
			continue
		}

		a, b, ok = tryPrefix(s, "rotate column x=", " by ")
		if ok {
			lcd.RotateColumn(a, b)
			continue
		}

		panic("bad s!")
	}

	return lcd.CalcPwr()
}
