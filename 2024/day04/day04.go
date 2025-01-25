package day04

import (
	"pshatov/aoc/year2024/util"
)

const Day = 4

var straightPattern = []byte("XMAS")
var reversedPattern []byte

var basePatternV2 = util.ByteField{
	{'M', 0, 0},
	{0, 'A', 0},
	{0, 0, 'S'},
}
var allPatternsV2 []util.ByteField

func rotatePatternV2(pattern util.ByteField) {
	p00 := pattern[0][0]
	p02 := pattern[0][2]
	p20 := pattern[2][0]
	p22 := pattern[2][2]
	pattern[0][0] = p20
	pattern[0][2] = p00
	pattern[2][0] = p22
	pattern[2][2] = p02
}

func addPatternV2(pattern, operand util.ByteField) {
	pattern[0][0] += operand[0][0]
	pattern[0][2] += operand[0][2]
	pattern[2][0] += operand[2][0]
	pattern[2][2] += operand[2][2]
}

func init() {
	for i := len(straightPattern); i > 0; i-- {
		reversedPattern = append(reversedPattern, straightPattern[i-1])
	}
	rotatedBasePatternV2 := basePatternV2.Copy()
	rotatePatternV2(rotatedBasePatternV2)
	for i := 0; i < 4; i++ {
		c := basePatternV2.Copy()
		allPatternsV2 = append(allPatternsV2, c)
	}
	rotatePatternV2(allPatternsV2[2])
	rotatePatternV2(allPatternsV2[2])
	rotatePatternV2(allPatternsV2[3])
	rotatePatternV2(allPatternsV2[3])
	addPatternV2(allPatternsV2[0], rotatedBasePatternV2)
	addPatternV2(allPatternsV2[2], rotatedBasePatternV2)
	rotatePatternV2(rotatedBasePatternV2)
	rotatePatternV2(rotatedBasePatternV2)
	addPatternV2(allPatternsV2[1], rotatedBasePatternV2)
	addPatternV2(allPatternsV2[3], rotatedBasePatternV2)
}

func findHorizontal(bf util.ByteField, output util.ByteField) int {
	total := 0
	total += findHorizontalWorker(bf, straightPattern, output)
	total += findHorizontalWorker(bf, reversedPattern, output)
	return total
}

func findVertical(bf util.ByteField, output util.ByteField) int {
	total := 0
	total += findVerticalWorker(bf, straightPattern, output)
	total += findVerticalWorker(bf, reversedPattern, output)
	return total
}

func findDiagonal(bf util.ByteField, output util.ByteField) int {
	total := 0
	total += findDiagonalDownwardWorker(bf, straightPattern, output)
	total += findDiagonalDownwardWorker(bf, reversedPattern, output)
	total += findDiagonalUpwardWorker(bf, straightPattern, output)
	total += findDiagonalUpwardWorker(bf, reversedPattern, output)
	return total
}

func findHorizontalWorker(bf util.ByteField, pattern []byte, output util.ByteField) int {
	total := 0
	for y := 0; y < bf.Dy(); y++ {
		for offset := 0; offset <= bf.Dx()-len(pattern); offset++ {
			valid := true
			for i := 0; i < len(pattern); i++ {
				if bf[y][offset+i] != pattern[i] {
					valid = false
					break
				}
			}
			if valid {
				for i := 0; i < len(pattern); i++ {
					output[y][offset+i] = pattern[i]
				}
				total++
			}
		}
	}
	return total
}

func findVerticalWorker(bf util.ByteField, pattern []byte, output util.ByteField) int {
	total := 0
	for x := 0; x < bf.Dx(); x++ {
		for offset := 0; offset <= bf.Dy()-len(pattern); offset++ {
			valid := true
			for i := 0; i < len(pattern); i++ {
				if bf[offset+i][x] != pattern[i] {
					valid = false
					break
				}
			}
			if valid {
				for i := 0; i < len(pattern); i++ {
					output[offset+i][x] = pattern[i]
				}
				total++
			}
		}
	}
	return total
}

func findDiagonalDownwardWorker(bf util.ByteField, pattern []byte, output util.ByteField) int {
	total := 0
	for y := 0; y <= bf.Dy()-len(pattern); y++ {
		for offset := 0; offset <= bf.Dx()-len(pattern); offset++ {
			valid := true
			for i := 0; i < len(pattern); i++ {
				if bf[y+i][offset+i] != pattern[i] {
					valid = false
					break
				}
			}
			if valid {
				for i := 0; i < len(pattern); i++ {
					output[y+i][offset+i] = pattern[i]
				}
				total++
			}
		}
	}
	return total
}

func findDiagonalUpwardWorker(bf util.ByteField, pattern []byte, output util.ByteField) int {
	total := 0
	for y := bf.Dy(); y >= len(pattern); y-- {
		for offset := 0; offset <= bf.Dx()-len(pattern); offset++ {
			valid := true
			for i := 0; i < len(pattern); i++ {
				if bf[y-i-1][offset+i] != pattern[i] {
					valid = false
					break
				}
			}
			if valid {
				for i := 0; i < len(pattern); i++ {
					output[y-i-1][offset+i] = pattern[i]
				}
				total++
			}
		}
	}
	return total
}

func findPatternV2(bf util.ByteField, pattern util.ByteField, output util.ByteField) int {
	total := 0
	for y := 0; y <= bf.Dy()-len(pattern); y++ {
		for x := 0; x <= bf.Dx()-len(pattern); x++ {
			valid := true
			for ty := 0; ty < pattern.Dy(); ty++ {
				for tx := 0; tx < pattern.Dx(); tx++ {
					if pattern[ty][tx] != 0 && bf[y+ty][x+tx] != pattern[ty][tx] {
						valid = false
						break
					}
				}
				if !valid {
					break
				}
			}
			if valid {
				for ty := 0; ty < pattern.Dy(); ty++ {
					for tx := 0; tx < pattern.Dx(); tx++ {
						if pattern[ty][tx] != 0 {
							output[y+ty][x+tx] = pattern[ty][tx]
						}
					}
				}
				total++
			}
		}
	}
	return total
}

func FindXMASv1(field util.StringField) (int, util.ByteField) {
	bf := field.ToByteField()
	output := field.ToByteField()
	output.Fill('.')

	total := 0
	total += findHorizontal(bf, output)
	total += findVertical(bf, output)
	total += findDiagonal(bf, output)

	return total, output
}

func FindXMASv2(field util.StringField) (int, util.ByteField) {
	bf := field.ToByteField()
	output := field.ToByteField()
	output.Fill('.')

	total := 0
	for _, pattern := range allPatternsV2 {
		total += findPatternV2(bf, pattern, output)
	}

	return total, output
}
