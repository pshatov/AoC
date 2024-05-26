package day10

import (
	"regexp"
	"slices"
	"strconv"
)

const DayNumber = 10

type Bot struct {
	NextBotLower, NextBotUpper       int
	NextOutputLower, NextOutputUpper int
	Values                           []int
	History                          []int
}

type Output struct {
	Values []int
}

func (b *Bot) Push(v int) {
	b.Values = append(b.Values, v)
}

func (o *Output) Push(v int) {
	o.Values = append(o.Values, v)
}

// TODO: Rewrite Push() using interfaces

type Bots map[int]*Bot
type Outputs map[int]*Output

func tryFindIndex(ln string, re *regexp.Regexp, indices *[]int) {

	matches := re.FindAllStringSubmatch(ln, -1)
	if matches == nil {
		return
	}

	for _, m := range matches {

		if len(m) != 2 {
			panic("bad match")
		}

		index, err := strconv.Atoi(m[1])
		if err != nil {
			panic("bad index")
		}

		if slices.Contains(*indices, index) {
			continue
		}

		*indices = append(*indices, index)
	}
}

func tryPushAll(bots Bots, outputs Outputs) bool {
	count := 0
	for _, b := range bots {
		count += b.tryPush(bots, outputs)
	}
	return count > 0
}

func (b *Bot) tryPush(bots Bots, outputs Outputs) int {

	if len(b.Values) >= 2 {

		valueLower := min(b.Values[0], b.Values[1])
		valueUpper := max(b.Values[0], b.Values[1])

		if b.NextBotLower >= 0 {
			bots[b.NextBotLower].Push(valueLower)
		} else {
			outputs[b.NextOutputLower].Push(valueLower)
		}

		if b.NextBotUpper >= 0 {
			bots[b.NextBotUpper].Push(valueUpper)
		} else {
			outputs[b.NextOutputUpper].Push(valueUpper)
		}

		if !slices.Contains(b.History, valueLower) {
			b.History = append(b.History, valueLower)
		}
		if !slices.Contains(b.History, valueUpper) {
			b.History = append(b.History, valueUpper)
		}

		b.Values = b.Values[2:]
		return 2
	}

	return 0
}

func FindBotAndOutputIndices(in []string) ([]int, []int) {

	reBot := regexp.MustCompile(`to bot (\d+)`)
	reOutput := regexp.MustCompile(`to output (\d+)`)

	bots := []int{}
	outputs := []int{}
	for _, ln := range in {

		tryFindIndex(ln, reBot, &bots)
		tryFindIndex(ln, reOutput, &outputs)
	}

	return bots, outputs
}

func CreateBotsAndOutputs(botIndices, outputIndices []int) (Bots, Outputs) {
	bots := make(Bots)
	outputs := make(Outputs)
	for _, index := range botIndices {
		bot := Bot{-1, -1, -1, -1, make([]int, 0), make([]int, 0)}
		bots[index] = &bot
	}
	for _, index := range outputIndices {
		output := Output{make([]int, 0)}
		outputs[index] = &output
	}
	return bots, outputs
}

func FindConnections(bots Bots, in []string) []string {

	re := regexp.MustCompile(`^bot (\d+) gives low to (bot|output) (\d+) and high to (bot|output) (\d+)$`)

	out := make([]string, 0)
	for _, ln := range in {
		m := re.FindStringSubmatch(ln)
		if m == nil {
			out = append(out, ln)
			continue
		}
		if len(m) != 6 {
			panic("wrong number of matches")
		}

		src, srcErr := strconv.Atoi(m[1])
		dstLower, dstLowerErr := strconv.Atoi(m[3])
		dstUpper, dstUpperErr := strconv.Atoi(m[5])
		if srcErr != nil || dstLowerErr != nil || dstUpperErr != nil {
			panic("can't convert bots")
		}

		_, okSrc := bots[src]
		_, okDstLower := bots[dstLower]
		_, okDstUpper := bots[dstUpper]

		if !okSrc || !okDstLower || !okDstUpper {
			panic("wrong bot")
		}

		// TODO: Add check for duplicate connections

		if m[2] == "bot" {
			bots[src].NextBotLower = dstLower
		} else {
			bots[src].NextOutputLower = dstLower
		}

		if m[4] == "bot" {
			bots[src].NextBotUpper = dstUpper
		} else {
			bots[src].NextOutputUpper = dstUpper
		}

	}

	return out
}

func InitValues(bots Bots, in []string) {

	re := regexp.MustCompile(`^value (\d+) goes to bot (\d+)$`)

	for _, ln := range in {
		m := re.FindStringSubmatch(ln)
		if m == nil {
			panic("can't parse")
		}
		if len(m) != 3 {
			panic("wrong number of matches")
		}

		value, valueErr := strconv.Atoi(m[1])
		index, indexErr := strconv.Atoi(m[2])
		if valueErr != nil || indexErr != nil {
			panic("can't convert")
		}

		_, okIndex := bots[index]
		if !okIndex {
			panic("wrong bot")
		}

		bots[index].Push(value)
	}
}

func Part1(in []string, target [2]int) (int, Outputs) {
	botIndices, outputIndices := FindBotAndOutputIndices(in)
	bots, outputs := CreateBotsAndOutputs(botIndices, outputIndices)
	in = FindConnections(bots, in)
	InitValues(bots, in)

	keepRunning := true
	for keepRunning {
		keepRunning = tryPushAll(bots, outputs)
	}

	minTarget := min(target[0], target[1])
	maxTarget := max(target[0], target[1])
	for i, b := range bots {
		if len(b.History) != 2 {
			panic("bad history")
		}
		if slices.Min(b.History) == minTarget &&
			slices.Max(b.History) == maxTarget {
			return i, outputs
		}
	}

	panic("target not found")
}
