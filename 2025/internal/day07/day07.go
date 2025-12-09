package day07

func CalcNumSplits(lines []string) int {
	dy := len(lines)
	dx := len(lines[dy-1])
	field := make([][]byte, dy)
	for y := range dy {
		field[y] = []byte(lines[y])
	}

	total := 0
	for y := range dy - 1 {
		for x := range dx {
			if y == 0 && field[y][x] == 'S' {
				field[y+1][x] = '|'
			}
			if y > 0 && field[y][x] == '|' {
				switch field[y+1][x] {
				case '.', '|':
					field[y+1][x] = '|'
				case '^':
					total += 1
					if /*x > 0 &&*/ field[y+1][x-1] != '^' {
						field[y+1][x-1] = '|'
					}
					if /*x < dx-1 &&*/ field[y+1][x+1] != '^' {
						field[y+1][x+1] = '|'
					}
				}
			}
		}
	}

	return total
}
