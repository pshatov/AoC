package day07

const (
	DayNumber = 7
)

func IsABBA(w string) bool {
	if len(w) != 4 {
		panic("Bad w length!")
	}
	ta := w[0] == w[3]
	tb := w[1] == w[2]
	tab := w[0] != w[1]
	return ta && tb && tab
}

func IsABA(w string) bool {
	if len(w) != 3 {
		panic("Bad w length!")
	}
	ta := w[0] == w[2]
	tab := w[0] != w[1]
	return ta && tab
}

func HasTLS(ip string) bool {
	abba, abbaHyper := false, false
	window, hyper := "", false
	// TODO: rewrite using slice of cap 4
	for _, r := range ip {
		switch r {

		case '[':
			if hyper {
				panic("Invalid hyper opening!")
			}
			window, hyper = "", true

		case ']':
			if !hyper {
				panic("Invalid hyper closing!")
			}
			window, hyper = "", false

		default:
			window += string(r)
			if len(window) > 4 {
				window = window[1:]
			}
			if len(window) == 4 {
				if t := IsABBA(window); t {
					if !hyper {
						abba = true
					} else {
						abbaHyper = true
					}
				}
			}
		}
	}

	return abba && !abbaHyper
}

func HasSSL(ip string) bool {
	abaSuper, babHyper := []string{}, []string{}
	window, super := "", true

	for _, r := range ip {
		switch r {

		case '[':
			if !super {
				panic("Invalid super opening!")
			}
			window, super = "", false

		case ']':
			if super {
				panic("Invalid super closing!")
			}
			window, super = "", true

		default:
			window += string(r)
			if len(window) > 3 {
				window = window[1:]
			}
			if len(window) == 3 {
				if t := IsABA(window); t {
					if super {
						abaSuper = append(abaSuper, window)
					} else {
						babHyper = append(babHyper, window)
					}
				}
			}
		}
	}

	for _, aba := range abaSuper {
		for _, bab := range babHyper {
			if aba[0] == bab[1] && aba[1] == bab[0] {
				return true
			}
		}
	}

	return false
}

func Part1(ips []string) int {
	result := 0
	for _, ip := range ips {
		if t := HasTLS(ip); t {
			result++
		}
	}
	return result
}

// TODO: Rewrite using function closures
func Part2(ips []string) int {
	result := 0
	for _, ip := range ips {
		if t := HasSSL(ip); t {
			result++
		}
	}
	return result
}
