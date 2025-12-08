package day05

import (
	"fmt"
	"slices"
	"sort"
	"strconv"
	"strings"
)

type IDRange struct {
	left, right int
}

type ID int

type Database struct {
	FreshRanges   []IDRange
	IngredientIDs []ID
}

type rangeNode struct {
	left, this, right IDRange
}

func ParseDatabase(lines []string) Database {
	db := Database{
		FreshRanges:   make([]IDRange, 0),
		IngredientIDs: make([]ID, 0),
	}
	for _, ln := range lines {
		parts := strings.Split(ln, "-")
		if n := len(parts); n == 1 {
			id, err := strconv.Atoi(parts[0])
			if err != nil {
				panic(fmt.Sprintf("can't parse database line '%s', bad id", ln))
			}
			db.IngredientIDs = append(db.IngredientIDs, ID(id))
		} else if n == 2 {
			left, err := strconv.Atoi(parts[0])
			if err != nil {
				panic(fmt.Sprintf("can't parse database line '%s', bad left part of range", ln))
			}
			right, err := strconv.Atoi(parts[1])
			if err != nil {
				panic(fmt.Sprintf("can't parse database line '%s', bad right part of range", ln))
			}
			db.FreshRanges = append(db.FreshRanges, IDRange{left, right})
		} else {
			panic(fmt.Sprintf("can't parse database line '%s', too many parts", ln))
		}
	}
	return db
}

func (id ID) InRange(r IDRange) bool {
	return ID(r.left) <= id && id <= ID(r.right)
}

func (id ID) IsFresh(ranges []IDRange) bool {
	return slices.ContainsFunc(ranges, id.InRange)
}

func (r IDRange) Len() int {
	return r.right - r.left + 1
}

func CalcFreshIngredients(db Database) int {
	total := 0
	for _, id := range db.IngredientIDs {
		if id.IsFresh(db.FreshRanges) {
			total++
		}
	}
	return total
}

func CalcFreshRanges(ranges []IDRange) int {
	sort.Slice(ranges, func(i, j int) bool {
		x, y := ranges[i], ranges[j]
		if x.left < y.left {
			return true
		} else if x.left == y.left {
			return x.right < y.right
		}
		return false
	})

	total := 0
	current := ranges[0]
	for i := 1; i < len(ranges); i++ {
		next := ranges[i]
		if next.left > current.right+1 {
			total += current.Len()
			current = next
			continue
		}
		if next.right > current.right {
			current.right = next.right
		}
	}
	total += current.Len()
	return total
}
