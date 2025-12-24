package day08

import (
	"aoc/2025/util"
	"container/heap"
	"fmt"
	"strconv"
	"strings"
)

type Dist struct {
	i, j, d2 int
}

type distHeap []Dist

func (h distHeap) Len() int {
	return len(h)
}

func (h distHeap) Less(i, j int) bool {
	return h[i].d2 > h[j].d2
}

func (h distHeap) Swap(i, j int) {
	h[i], h[j] = h[j], h[i]
}

func (h *distHeap) Push(x any) {
	*h = append(*h, x.(Dist))
}

func (h *distHeap) Pop() any {
	old := *h
	n := len(old)
	x := old[n-1]
	*h = old[0 : n-1]
	return x
}

func parseLines(lines []string) []util.XYZ {
	result := []util.XYZ{}
	for _, ln := range lines {
		parts := strings.Split(ln, ",")
		if n := len(parts); n != 3 {
			panic(fmt.Errorf("bad line '%s', expected 3 parts, but has %d", ln, n))
		}
		x, err := strconv.Atoi(parts[0])
		if err != nil {
			panic(fmt.Errorf("bad x part in line '%s'", ln))
		}
		y, err := strconv.Atoi(parts[1])
		if err != nil {
			panic(fmt.Errorf("bad y part in line '%s'", ln))
		}
		z, err := strconv.Atoi(parts[2])
		if err != nil {
			panic(fmt.Errorf("bad z part in line '%s'", ln))
		}
		result = append(result, util.XYZ{X: x, Y: y, Z: z})
	}
	return result
}

func calcDist2(a, b util.XYZ) int {
	dx := a.X - b.X
	dy := a.Y - b.Y
	dz := a.Z - b.Z
	return dx*dx + dy*dy + dz*dz
}

func getDists(boxes []util.XYZ, count int) distHeap {
	dists := distHeap{}
	h := (heap.Interface)(&dists)
	for i := 0; i < len(boxes)-1; i++ {
		for j := i + 1; j < len(boxes); j++ {
			d2 := calcDist2(boxes[i], boxes[j])
			tmp := Dist{i: i, j: j, d2: d2}
			if h.Len() < count {
				heap.Push(h, tmp)
			} else if tmp.d2 < dists[0].d2 {
				heap.Pop(h)
				heap.Push(h, tmp)
			}
		}
	}
	return dists
}

func CalcPart1(boxes []util.XYZ, count int) int {
	dists := getDists(boxes, count)
	nextIndex := 0
	indices := make([]int, len(boxes))
	for _, d := range dists {
		if indices[d.i] == 0 {
			if indices[d.j] == 0 {
				nextIndex++
				indices[d.i] = nextIndex
				indices[d.j] = nextIndex
			} else {
				indices[d.i] = indices[d.j]
			}
		} else {
			if indices[d.j] == 0 {
				indices[d.j] = indices[d.i]
			} else {
				new, old := indices[d.i], indices[d.j]
				for k := range boxes {
					if indices[k] == old {
						indices[k] = new
					}
				}
			}
		}
	}
	lengths := make(map[int]int)
	for k := range boxes {
		if indices[k] > 0 {
			lengths[indices[k]]++
		}
	}
	result := 1
	for range 3 {
		maxLen := 0
		maxIndex := -1
		for i, l := range lengths {
			if l > maxLen {
				maxLen = l
				maxIndex = i
			}
		}
		result *= maxLen
		delete(lengths, maxIndex)
	}
	// 12160 too low
	// 20181 too low
	return result
}
