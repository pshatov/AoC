package day09_test

import (
	"pshatov/aoc/year2016/day09"
	"pshatov/aoc/year2016/day09/vectors"
	"testing"
	"unicode/utf8"
)

func testProcV1(t *testing.T, v *vectors.VectorInline) {

	if v.Want == 0 || (len(v.Out) > 0 && v.Want != utf8.RuneCountInString(v.Out)) {
		panic("inconsistent vector")
	}

	got := day09.DecompressV1(v.In)
	if len(v.Out) > 0 {
		if got != v.Out {
			t.Errorf("got == %#v, want %#v", got, v.Out)
		}
	}

	if n := utf8.RuneCountInString(got); n != v.Want {
		t.Errorf("len(got) == %#v, want %#v", n, v.Want)
	}
}

func testProcV2(t *testing.T, v *vectors.VectorInline) {

	if v.Want == 0 && len(v.Out) == 0 {
		panic("invalid vector")
	}

	if v.Want == 0 {
		v.Want = utf8.RuneCountInString(v.Out)
	}

	if len(v.Out) > 0 && v.Want != utf8.RuneCountInString(v.Out) {
		panic("inconsistent vector")
	}

	got := day09.DecompressV2(v.In)
	if got != v.Want {
		t.Errorf("got == %#v, want %#v", got, v.Want)
	}
}

func TestPart1Examples(t *testing.T) {
	for _, v := range vectors.ExamplesV1 {
		testProcV1(t, &v)
	}
}

func TestPart1Input(t *testing.T) {
	v := vectors.InputV1.ToInline(t)
	testProcV1(t, &v)
}

func TestPart2Examples(t *testing.T) {
	for _, v := range vectors.ExamplesV2 {
		testProcV2(t, &v)
	}
}

func TestPart2Input(t *testing.T) {
	v := vectors.InputV2.ToInline(t)
	testProcV2(t, &v)
}
