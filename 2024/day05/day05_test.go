package day05_test

import (
	"fmt"
	"pshatov/aoc/year2024/day05"
	"pshatov/aoc/year2024/util"
	"strconv"
	"strings"
	"testing"

	"github.com/stretchr/testify/assert"
)

func parsePart(part string, index int) int {
	v, err := strconv.Atoi(part)
	if err != nil {
		panic(fmt.Errorf("bad input line #%d: can't parse part %s", index+1, part))
	}
	return v
}

func parseData(lines []string) (rules []day05.Rule, updates []day05.Update) {
	for i, ln := range lines {
		parts := strings.Split(ln, "|")
		if len(parts) > 1 {
			if len(parts) != 2 {
				panic(fmt.Errorf("bad rule line '%s': must have two parts, but has %d", ln, len(parts)))
			}
			var r day05.Rule
			r.X = parsePart(parts[0], i)
			r.Y = parsePart(parts[1], i)
			rules = append(rules, r)
			continue
		}
		parts = strings.Split(ln, ",")
		if len(parts) > 1 {
			var u day05.Update
			for _, p := range parts {
				n := parsePart(p, i)
				u = append(u, n)
			}
			updates = append(updates, u)
			continue
		}
		panic(fmt.Errorf("bad input line '%s': can't split", ln))
	}
	return
}

func TestPart1(t *testing.T) {
	for _, tc := range []struct {
		data              string
		total, totalFixed int
	}{
		{"example", 143, 123},
		{"input", 5747, 5502},
	} {
		lines := util.LoadData("..", day05.Day, tc.data)
		rules, updates := parseData(lines)
		total, totalFixed := day05.SovleParts(rules, updates)
		assert.Equal(t, tc.total, total)
		assert.Equal(t, tc.totalFixed, totalFixed)
	}
}
