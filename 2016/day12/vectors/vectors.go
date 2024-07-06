package vectors

import "pshatov/aoc/year2016/day12"

type TestVector struct {
	Program day12.ProgramStr
	Result  int
}

var (
	VectorExample = TestVector{
		day12.ProgramStr{
			"cpy 41 a",
			"inc a",
			"inc a",
			"dec a",
			"jnz a 2",
			"dec a",
		},
		42}
	VectorPart1 = TestVector{
		day12.ProgramStr{
			"cpy 1 a",
			"cpy 1 b",
			"cpy 26 d",
			"jnz c 2",
			"jnz 1 5",
			"cpy 7 c",
			"inc d",
			"dec c",
			"jnz c -2",
			"cpy a c",
			"inc a",
			"dec b",
			"jnz b -2",
			"cpy c b",
			"dec d",
			"jnz d -6",
			"cpy 17 c",
			"cpy 18 d",
			"inc a",
			"dec d",
			"jnz d -2",
			"dec c",
			"jnz c -5",
		},
		318117}
	VectorPart2 = TestVector{
		VectorPart1.Program,
		9227771}
)
