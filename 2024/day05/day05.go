package day05

import (
	"errors"
	"fmt"
	"slices"
)

const Day = 5

type Rule struct {
	X, Y int
}

type Update []int

func (u Update) Valid(rules []Rule) bool {
	for _, r := range rules {
		ix := u.Index(r.X)
		iy := u.Index(r.Y)
		if ix < 0 || iy < 0 {
			continue
		}
		if iy < ix {
			return false
		}
	}
	return true
}

func (u Update) Index(page int) int {
	return slices.Index(u, page)
}

func (u Update) Middle() int {
	if len(u)%2 == 0 {
		panic(fmt.Errorf("update length must be odd, but is %d", len(u)))
	}
	index := (len(u) - 1) / 2
	return u[index]
}

func (u Update) Fix(rules []Rule) Update {
	var relevantRules []Rule
	for _, r := range rules {
		if u.Index(r.X) < 0 || u.Index(r.Y) < 0 {
			continue
		}
		relevantRules = append(relevantRules, r)
	}
	leftNeighbors := make(map[int][]int)
	for _, p := range u {
		leftNeighbors[p] = []int{}
	}
	for _, p := range u {
		for _, r := range relevantRules {
			if r.Y == p {
				leftNeighbors[p] = append(leftNeighbors[p], r.X)
			}
		}
	}
	var output []int
	for len(leftNeighbors) > 0 {
		foundNext := false
		nextPage := -1
		for p := range leftNeighbors {
			if len(leftNeighbors[p]) == 0 {
				nextPage = p
				foundNext = true
				break
			}
		}
		if !foundNext {
			panic(errors.New("internal error"))
		}
		output = append(output, nextPage)
		delete(leftNeighbors, nextPage)
		for p := range leftNeighbors {
			i := slices.Index(leftNeighbors[p], nextPage)
			if i >= 0 {
				leftNeighbors[p] = append(leftNeighbors[p][:i], leftNeighbors[p][i+1:]...)
			}
		}
	}
	return output
}

func SovleParts(rules []Rule, updates []Update) (total, totalFixed int) {
	for _, u := range updates {
		if u.Valid(rules) {
			total += u.Middle()
		} else {
			fixed := u.Fix(rules)
			totalFixed += fixed.Middle()
		}
	}
	return
}
