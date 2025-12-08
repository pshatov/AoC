package day05

import (
	"fmt"
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
	for _, r := range ranges {
		if id.InRange(r) {
			return true
		}
	}
	return false
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
