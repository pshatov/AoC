package vectors

type TestVector struct {
	Seed  string
	Index int
}

type FindRepeatsVector struct {
	Hash    string
	Length  int
	Symbols []rune
}

var (
	VectorsFindRepeats = []FindRepeatsVector{
		{"zvz", 3, []rune{}},
		{"zzz", 3, []rune{'z'}},
		{"zzzz", 3, []rune{'z'}},
		{"vzzz", 3, []rune{'z'}},
		{"zzzv", 3, []rune{'z'}},
		{"vzzzv", 3, []rune{'z'}},
		{"zzzooo", 3, []rune{'z', 'o'}},
		{"vzzzooo", 3, []rune{'z', 'o'}},
		{"zzzvooo", 3, []rune{'z', 'o'}},
		{"zzzooov", 3, []rune{'z', 'o'}},
		{"vzzzvooo", 3, []rune{'z', 'o'}},
		{"vzzzooov", 3, []rune{'z', 'o'}},
		{"zzzvooov", 3, []rune{'z', 'o'}},
		{"vzzzvooov", 3, []rune{'z', 'o'}},
		{"vzzzvzzzv", 3, []rune{'z'}},
		{"zzvzz", 5, []rune{}},
		{"zzzzz", 5, []rune{'z'}},
		{"vzzzzz", 5, []rune{'z'}},
		{"zzzzzv", 5, []rune{'z'}},
		{"vzzzzzvzzzzzv", 5, []rune{'z'}},
		{"zzzzzvvvvv", 5, []rune{'z', 'v'}},
		{"ozzzzzvvvvv", 5, []rune{'z', 'v'}},
		{"zzzzzovvvvv", 5, []rune{'z', 'v'}},
		{"zzzzzvvvvvo", 5, []rune{'z', 'v'}},
		{"ozzzzzovvvvv", 5, []rune{'z', 'v'}},
		{"ozzzzzvvvvvo", 5, []rune{'z', 'v'}},
		{"zzzzzovvvvvo", 5, []rune{'z', 'v'}},
		{"ozzzzzovvvvvo", 5, []rune{'z', 'v'}},
	}
	VectorExample1 = TestVector{"abc", 22728}
	VectorPart1    = TestVector{"ihaygndm", 15035}
	VectorExample2 = TestVector{"abc", 22551}
	VectorPart2    = TestVector{"ihaygndm", 19968}
)
