package util

import (
	"aoc/2025/testutil"
	"testing"
)

const (
	intEmpty = 0
	sampleDx = 5
	sampleDy = 4
)

var sampleMaze = []string{
	".....",
	".....",
	".....",
	".....",
}

var sampleKey = map[byte]int{'.': intEmpty}

func TestMazeAddBorder(t *testing.T) {
	m := NewMazeFromLines(sampleMaze, sampleKey)
	m.AddBorder(intEmpty)
	if m.dx != sampleDx+2 {
		t.Fatalf("AddBorder(): dx = %d, but must be %d", m.dx, sampleDx+2)
	}
	if m.dy != sampleDy+2 {
		t.Fatalf("AddBorder(): dy = %d, but must be %d", m.dy, sampleDy+2)
	}
	if !m.hasBorder {
		t.Fatalf("AddBorder(): hasBorder = %v, but must be %v", m.hasBorder, true)
	}
}

func TestMazeRemoveBorder(t *testing.T) {
	m := NewMazeFromLines(sampleMaze, sampleKey)
	m.hasBorder = true
	m.RemoveBorder()
	if m.dx != sampleDx-2 {
		t.Fatalf("RemoveBorder(): dx = %d, but must be %d", m.dx, sampleDx-2)
	}
	if m.dy != sampleDy-2 {
		t.Fatalf("RemoveBorder(): dy = %d, but must be %d", m.dy, sampleDy-2)
	}
	if m.hasBorder {
		t.Fatalf("AddBorder(): hasBorder = %v, but must be %v", m.hasBorder, false)
	}
}

func TestMazeAddBorderTwice(t *testing.T) {
	m := NewMazeFromLines(sampleMaze, sampleKey)
	t.Run("add_border_twice", func(t *testing.T) {
		testutil.MustPanic(t, func() {
			m.AddBorder(intEmpty)
			m.AddBorder(intEmpty)
		})
	})
}

func TestMazeRemoveBorderTwice(t *testing.T) {
	m := NewMazeFromLines(sampleMaze, sampleKey)
	t.Run("remove_border_twice", func(t *testing.T) {
		testutil.MustPanic(t, func() {
			m.hasBorder = true
			m.RemoveBorder()
			m.RemoveBorder()
		})
	})
}
