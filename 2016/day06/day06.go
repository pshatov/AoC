package day06

const (
	DayNumber = 6
)

type RuneFreq map[rune]int

func addRuneFreq(freqs []RuneFreq, m string) []RuneFreq {

	// special case for the very fist call
	if len(freqs) == 0 {
		for i := 0; i < len(m); i++ {
			freqs = append(freqs, RuneFreq{})
		}
	}

	// sanity check
	if len(freqs) != len(m) {
		panic("Bad length of m!")
	}

	for pos, r := range m {
		_, ok := freqs[pos][r]
		if !ok {
			freqs[pos][r] = 0
		}
		freqs[pos][r]++
	}

	return freqs
}

func Part1(msgs []string) string {

	freqs := []RuneFreq{}
	for _, m := range msgs {
		freqs = addRuneFreq(freqs, m)
	}

	result := ""
	for i := 0; i < len(freqs); i++ {
		maxFreq, maxRune := 0, '?'
		for k, v := range freqs[i] {
			if v > maxFreq {
				maxFreq = v
				maxRune = k
			}
		}

		result += string(maxRune)
	}

	return result
}

// TODO: Rewrite using closure (freq-based rune picker)
func Part2(msgs []string) string {
	freqs := []RuneFreq{}
	for _, m := range msgs {
		freqs = addRuneFreq(freqs, m)
	}

	result := ""
	for i := 0; i < len(freqs); i++ {
		minFreq, minRune := len(msgs), '?'
		for k, v := range freqs[i] {
			if v < minFreq {
				minFreq = v
				minRune = k
			}
		}

		result += string(minRune)
	}

	return result
}
