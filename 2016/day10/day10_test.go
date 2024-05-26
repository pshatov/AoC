package day10_test

import (
	"pshatov/aoc/year2016/day10"
	"pshatov/aoc/year2016/day10/vectors"
	"testing"
)

const wantPart2 = 133163

func TestPart1Example(t *testing.T) {
	got, _ := day10.Part1(vectors.Example.In, vectors.Example.Target)
	if got != vectors.Example.Want {
		t.Errorf("Part1(): got == %#v, want %#v", got, vectors.Example.Want)
	}
}

func TestPart1Input(t *testing.T) {
	vectorInput := vectors.Input.ToInline(t)
	got, _ := day10.Part1(vectorInput.In, vectorInput.Target)
	if got != vectorInput.Want {
		t.Errorf("Part1(): got == %#v, want %#v", got, vectorInput.Want)
	}
}

func TestPart2Input(t *testing.T) {
	vectorInput := vectors.Input.ToInline(t)
	_, outputs := day10.Part1(vectorInput.In, vectorInput.Target)

	out0, ok0 := outputs[0]
	out1, ok1 := outputs[1]
	out2, ok2 := outputs[2]

	if !ok0 || !ok1 || !ok2 {
		t.Errorf("Part2(): missing one or more of required outputs")
	} else {
		if len(out0.Values) != 1 || len(out1.Values) != 1 || len(out2.Values) != 1 {
			t.Errorf("Part2(): wrong length of one or more of required outputs")
		} else {
			p := 1
			p *= out0.Values[0]
			p *= out1.Values[0]
			p *= out2.Values[0]
			if p != wantPart2 {
				t.Errorf("Part2(): got == %#v, want == %#v", p, wantPart2)
			}
		}
	}
}
