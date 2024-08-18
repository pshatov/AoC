package day14_test

import (
	"pshatov/aoc/year2016/day14"
	"pshatov/aoc/year2016/day14/vectors"
	"testing"
)

func TestFindRepeats(t *testing.T) {
	for _, vec := range vectors.VectorsFindRepeats {
		got := day14.FindRepeats(vec.Hash, vec.Length)
		if len(got) != len(vec.Symbols) {
			t.Logf("TestFindRepeats(%s): len(got) == %#v, len(want) == %#v",
				vec.Hash, len(got), len(vec.Symbols))
			t.FailNow()
		}
		for i := 0; i < len(got); i++ {
			if got[i] != vec.Symbols[i] {
				t.Errorf("TestFindRepeats(%s): got[%d] == %#v, want[%d] == %#v",
					vec.Hash, i, got, i, vec.Symbols[i])
			}
		}
	}
}

func TestExample1(t *testing.T) {
	vec := vectors.VectorExample1
	got := day14.GenerateKeys(vec.Seed, false)
	if got != vec.Index {
		t.Errorf("TestExample1(): got == %#v, want == %#v", got, vec.Index)
	}
}

func TestExample2(t *testing.T) {
	vec := vectors.VectorExample2
	got := day14.GenerateKeys(vec.Seed, true)
	if got != vec.Index {
		t.Errorf("TestExample2(): got == %#v, want == %#v", got, vec.Index)
	}
}

func TestPart1(t *testing.T) {
	vec := vectors.VectorPart1
	got := day14.GenerateKeys(vec.Seed, false)
	if got != vec.Index {
		t.Errorf("TestPart1(): got == %#v, want == %#v", got, vec.Index)
	}
}

func TestPart2(t *testing.T) {
	vec := vectors.VectorPart2
	got := day14.GenerateKeys(vec.Seed, true)
	if got != vec.Index {
		t.Errorf("TestPart2(): got == %#v, want == %#v", got, vec.Index)
	}
}
