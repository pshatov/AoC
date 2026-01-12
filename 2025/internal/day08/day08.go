package day08

import (
	"aoc/2025/util"
	"container/heap"
	"fmt"
	"slices"
	"strconv"
	"strings"
)

type Dist struct {
	i, j, d2 int
}

type distHeap struct {
	data []Dist
	max  bool
}

func (h distHeap) Len() int {
	return len(h.data)
}

func (h distHeap) Less(i, j int) bool {
	d2i, d2j := h.data[i].d2, h.data[j].d2
	if h.max {
		return d2i < d2j
	}
	return d2i > d2j
}

func (h distHeap) Swap(i, j int) {
	h.data[i], h.data[j] = h.data[j], h.data[i]
}

func (h *distHeap) Push(x any) {
	h.data = append(h.data, x.(Dist))
}

func (h *distHeap) Pop() any {
	old := h.data
	n := len(old)
	x := old[n-1]
	h.data = old[0 : n-1]
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

func getDists(boxes []util.XYZ, count int, max bool) distHeap {
	dists := distHeap{max: max}
	h := (heap.Interface)(&dists)
	for i := 0; i < len(boxes)-1; i++ {
		for j := i + 1; j < len(boxes); j++ {
			d2 := calcDist2(boxes[i], boxes[j])
			tmp := Dist{i: i, j: j, d2: d2}
			if h.Len() < count {
				heap.Push(h, tmp)
			} else if tmp.d2 < dists.data[0].d2 {
				heap.Pop(h)
				heap.Push(h, tmp)
			}
		}
	}
	return dists
}

func addCircuit(d Dist, circuits []int, nextIndex int) int {
	if circuits[d.i] == 0 {
		if circuits[d.j] == 0 {
			nextIndex++
			circuits[d.i] = nextIndex
			circuits[d.j] = nextIndex
		} else {
			circuits[d.i] = circuits[d.j]
		}
	} else {
		if circuits[d.j] == 0 {
			circuits[d.j] = circuits[d.i]
		} else {
			new, old := circuits[d.i], circuits[d.j]
			for k := range circuits {
				if circuits[k] == old {
					circuits[k] = new
				}
			}
		}
	}

	return nextIndex
}

func CalcPart1(boxes []util.XYZ, count int) int {
	dists := getDists(boxes, count, false)
	nextIndex := 0
	circuits := make([]int, len(boxes))
	for dists.Len() > 0 {
		d := heap.Pop(&dists).(Dist)
		nextIndex = addCircuit(d, circuits, nextIndex)
	}
	lengths := make(map[int]int)
	for k := range boxes {
		if circuits[k] > 0 {
			lengths[circuits[k]]++
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
	return result
}

func CalcPart2(boxes []util.XYZ) int {
	n := len(boxes)
	dists := getDists(boxes, n*(n-1)/2, true)
	nextIndex := 0
	circuits := make([]int, len(boxes))
	var d Dist
	for dists.Len() > 0 {
		d = heap.Pop(&dists).(Dist)
		nextIndex = addCircuit(d, circuits, nextIndex)
		if slices.Contains(circuits, 0) {
			continue
		}
		sameCircuit := true
		for k := 1; k < n; k++ {
			if circuits[k] != circuits[0] {
				sameCircuit = false
				break
			}
		}
		if !sameCircuit {
			continue
		}
		break
	}
	result := 1
	result *= boxes[d.i].X
	result *= boxes[d.j].X
	return result
}
