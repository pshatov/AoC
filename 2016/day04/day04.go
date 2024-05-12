package day04

import (
	"sort"
	"strconv"
	"strings"
)

type Room struct {
	name     string
	sector   int
	checksum string
}

const (
	TargetRoom string = "northpole object storage"
)

func (room *Room) IsValid() bool {

	runeFreqs := make(map[rune]int)
	freqRunes := []rune{}

	for _, r := range room.name {
		if r == '-' {
			continue
		}
		f, ok := runeFreqs[r]
		if !ok {
			freqRunes = append(freqRunes, r)
			f = 1
		} else {
			f++
		}
		runeFreqs[r] = f
	}

	if l := len(runeFreqs); l < 5 {
		panic("less than five rune freqs!")
	}

	sort.Slice(freqRunes, func(i, j int) bool {
		return freqRunes[i] < freqRunes[j]
	})

	refChecksum := make([]rune, len(room.checksum))
	for i := 0; i < len(refChecksum); i++ {
		runeRef, freqRef := '?', -1
		for _, r := range freqRunes {
			f := runeFreqs[r]
			if freqRef < 0 || f > freqRef {
				runeRef, freqRef = r, f
			}
		}
		runeFreqs[runeRef] = -1
		refChecksum[i] = runeRef
	}

	strChecksum := string(refChecksum)

	return room.checksum == strChecksum
}

func rotateRune(c rune, n int) rune {
	for c += rune(n); c > 'z'; c -= ('z' - 'a' + 1) {
	}
	return c
}

func (room *Room) Decrypt() string {
	result := []rune{}
	for _, c := range room.name {
		if c == '-' {
			c = ' '
		} else {
			c = rotateRune(c, room.sector)
		}
		result = append(result, c)
	}
	return string(result)
}

func parseNameSector(left string) (name string, sector int) {
	i := strings.LastIndex(left, "-")
	name, middle := left[:i], left[i+1:]

	sector, err := strconv.Atoi(middle)
	if err != nil {
		panic("bad sector!")
	}

	return
}

func ParseRoom(line string) Room {
	line, ok := strings.CutSuffix(line, "]")
	if !ok {
		panic("bad suffix!")
	}

	left, checksum, ok := strings.Cut(line, "[")
	if !ok {
		panic("can't cut!")
	}

	if t := len(checksum); t != 5 {
		panic("bad checksum length")
	}

	name, sector := parseNameSector(left)

	return Room{name, sector, checksum}
}

func Part1(lines []string) int {
	n := 0
	for _, ln := range lines {
		r := ParseRoom(ln)
		if ok := r.IsValid(); ok {
			n += r.sector
		}
	}
	return n
}

func Part2(lines []string) int {
	for _, ln := range lines {
		r := ParseRoom(ln)
		t := r.Decrypt()
		if t == TargetRoom {
			return r.sector
		}
	}
	panic("target room not found!")
}
