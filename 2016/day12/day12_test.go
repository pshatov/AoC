package day12_test

import (
	"pshatov/aoc/year2016/day12"
	"pshatov/aoc/year2016/day12/vectors"
	"testing"
)

func TestExample(t *testing.T) {
	vec := vectors.VectorExample
	state := day12.RegState{}
	day12.RunProgram(vec.Program, &state)
	if state.A != vec.Result {
		t.Errorf("Example(): got == %#v, want %#v", state.A, vec.Result)
	}
}

func TestPart1(t *testing.T) {
	vec := vectors.VectorPart1
	state := day12.RegState{}
	day12.RunProgram(vec.Program, &state)
	if state.A != vec.Result {
		t.Errorf("Example(): got == %#v, want %#v", state.A, vec.Result)
	}
}

func TestPart2(t *testing.T) {
	vec := vectors.VectorPart2
	state := day12.RegState{}
	state.C = 1
	day12.RunProgram(vec.Program, &state)
	if state.A != vec.Result {
		t.Errorf("Example(): got == %#v, want %#v", state.A, vec.Result)
	}
}
