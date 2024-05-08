package day02

type Pos struct {
	R, C int
}

var Pad1 = [][]rune{
	{'1', '2', '3'},
	{'4', '5', '6'},
	{'7', '8', '9'},
}

var Pad2 = [][]rune{
	{'?', '?', '1', '?', '?'},
	{'?', '2', '3', '4', '?'},
	{'5', '6', '7', '8', '9'},
	{'?', 'A', 'B', 'C', '?'},
	{'?', '?', 'D', '?', '?'},
}

func LookupPad1(pos Pos) string {
	return string(Pad1[pos.R][pos.C])
}

func LookupPad2(pos Pos) string {
	return string(Pad2[pos.R][pos.C])
}

// TODO: Consider rewriting using function closures

func nextPos1(pos Pos, move rune) Pos {
	switch move {
	case 'U':
		if pos.R > 0 {
			pos.R--
		}
	case 'D':
		if pos.R < 2 {
			pos.R++
		}
	case 'L':
		if pos.C > 0 {
			pos.C--
		}
	case 'R':
		if pos.C < 2 {
			pos.C++
		}
	default:
		panic("bad move!")
	}
	return pos
}

func nextPos2(pos Pos, move rune) Pos {
	switch move {
	case 'U':
		if pos.R > 0 {
			pos.R--
		}
	case 'D':
		if pos.R < 4 {
			pos.R++
		}
	case 'L':
		if pos.C > 0 {
			pos.C--
		}
	case 'R':
		if pos.C < 4 {
			pos.C++
		}
	default:
		panic("bad move!")
	}
	return pos
}

func Part1(doc []string) string {
	pos, code := Pos{1, 1}, ""
	for _, line := range doc {
		for _, move := range line {
			pos = nextPos1(pos, move)
		}
		code += LookupPad1(pos)
	}
	return string(code)
}

func Part2(doc []string) string {
	pos, code := Pos{2, 0}, ""
	for _, line := range doc {
		for _, move := range line {
			posNew := nextPos2(pos, move)
			sym := LookupPad2(posNew)
			if sym != "?" {
				pos = posNew
			}
		}
		code += LookupPad2(pos)
	}
	return string(code)
}
