package util

import (
	"fmt"
)

type Maze struct {
	dx, dy    int
	hasBorder bool
	matrix    [][]int
	printKey  map[int]byte
}

func NewMazeFromLines(lines []string, key map[byte]int) Maze {
	matrix := make([][]int, len(lines))
	printKey := make(map[int]byte)
	for k, v := range key {
		_, ok := printKey[v]
		if ok {
			panic(fmt.Sprintf("invalid maze key, duplicate entry '%d'", v))
		}
		printKey[v] = k
	}
	dy := len(lines)
	if dy < 2 {
		panic(fmt.Sprintf("bad maze y size %d", dy))
	}
	dx := len(lines[0])
	for y := range dy {
		ln := lines[y]
		if len(ln) != dx {
			panic(fmt.Sprintf("maze line %d length is %d, but the first line has length %d", y, len(ln), dx))
		}
		matrix[y] = make([]int, dx)
		for x := range dx {
			ch := ln[x]
			sym, ok := key[ch]
			if !ok {
				panic(fmt.Sprintf("invalid byte '%v' on line %d at offset %d", ch, y, x))
			}
			matrix[y][x] = sym
		}
	}
	return Maze{
		dx:        dx,
		dy:        dy,
		hasBorder: false,
		matrix:    matrix,
		printKey:  printKey,
	}
}

func (m *Maze) Dy() int {
	return m.dy
}

func (m *Maze) Dx() int {
	return m.dx
}

func (m *Maze) HasBorder() bool {
	return m.hasBorder
}

func (m *Maze) At(y, x int) int {
	return m.matrix[y][x]
}

func (m *Maze) Set(y, x int, value int) {
	m.matrix[y][x] = value
}

func (m *Maze) AddBorder(value int) {
	if m.hasBorder {
		panic("border already added")
	}
	for y := range m.dy {
		m.matrix[y] = append([]int{value}, m.matrix[y]...)
		m.matrix[y] = append(m.matrix[y], value)
	}
	m.dx += 2
	m.dy += 2
	m.matrix = append([][]int{make([]int, m.dx)}, m.matrix...)
	m.matrix = append(m.matrix, make([]int, m.dx))
	for x := range m.dx {
		m.matrix[0][x] = value
		m.matrix[m.dy-1][x] = value
	}
	m.hasBorder = true
}

func (m *Maze) RemoveBorder() {
	if !m.hasBorder {
		panic("no border to remove")
	}
	for y := 1; y < m.dy-1; y++ {
		m.matrix[y] = m.matrix[y][1 : m.dx-1]
	}
	m.dx -= 2
	m.matrix = m.matrix[1 : m.dy-1]
	m.dy -= 2
	m.hasBorder = false
}

func (m *Maze) DebugPrint() {
	for y := range m.Dy() {
		for x := range m.Dx() {
			fmt.Print(string(m.printKey[m.matrix[y][x]]))
		}
		fmt.Println("")
	}
}
