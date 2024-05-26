package day09

import (
	"regexp"
	"strconv"
	"strings"
	"unicode/utf8"
)

const (
	DayNumber = 9
)

func DecompressV1(data string) string {

	buf := ""
	for len(data) > 0 {
		r, s := utf8.DecodeRuneInString(data)
		if r != '(' {
			buf += string(r)
			data = data[s:]
			continue
		}

		re := regexp.MustCompile(`^\((\d+)x(\d+)\)`)
		m := re.FindStringSubmatch(data)
		if m == nil || len(m) != 3 {
			panic("can't parse marker")
		}

		window, windowErr := strconv.Atoi(m[1])
		repeat, repeatErr := strconv.Atoi(m[2])

		if windowErr != nil || repeatErr != nil {
			panic("bad marker")
		}

		var cutOk bool
		data, cutOk = strings.CutPrefix(data, m[0])
		if !cutOk {
			panic("can't cut marker")
		}

		part := string([]rune(data)[:window])
		data, cutOk = strings.CutPrefix(data, part)
		if !cutOk {
			panic("can't cut part")
		}

		for r := 0; r < repeat; r++ {
			buf = buf + part
		}
	}

	return string(buf)
}

func DecompressV2(data string) int {

	size := 0

	for len(data) > 0 {
		r, s := utf8.DecodeRuneInString(data)
		if r != '(' {
			size++
			data = data[s:]
			continue
		}

		re := regexp.MustCompile(`^\((\d+)x(\d+)\)`)
		m := re.FindStringSubmatch(data)
		if m == nil || len(m) != 3 {
			panic("can't parse marker")
		}

		window, windowErr := strconv.Atoi(m[1])
		repeat, repeatErr := strconv.Atoi(m[2])

		if windowErr != nil || repeatErr != nil {
			panic("bad marker")
		}

		var cutOk bool
		data, cutOk = strings.CutPrefix(data, m[0])
		if !cutOk {
			panic("can't cut marker")
		}

		part := string([]rune(data)[:window])
		data, cutOk = strings.CutPrefix(data, part)
		if !cutOk {
			panic("can't cut part")
		}

		size += repeat * DecompressV2(part)
	}

	return size
}
