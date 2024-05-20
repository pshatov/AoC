package day08_test

import (
	"fmt"
	"pshatov/aoc/year2016/day08"
	"pshatov/aoc/year2016/day08/vectors"
	"testing"
)

func testVector(t *testing.T, v *vectors.TestCaseInline) {

	lcd := day08.MakeLCD(v.W, v.H)
	pwr := day08.Part(v.In, lcd)

	if v.Want > 0 && pwr != v.Want {
		t.Errorf("pwr == %#v, expect %#v", pwr, v.Want)
	}

	if len(v.Out) == 0 {
		for y := 0; y < len(lcd.Dots); y++ {
			fmt.Println(lcd.Dots[y])
		}
		panic("missing out!")
	}

	for y := 0; y < lcd.H; y++ {
		if lcd.Dots[y] != v.Out[y] {
			t.Errorf("lcd.Dots[%#v] == %#v, expect %#v", y, lcd.Dots[y], v.Out[y])
		}
	}
}

func TestPartExample(t *testing.T) {
	testVector(t, &vectors.CaseExample)
}

func TestPartInput(t *testing.T) {
	v := vectors.CaseInput.ToInline(t)
	testVector(t, v)
}
