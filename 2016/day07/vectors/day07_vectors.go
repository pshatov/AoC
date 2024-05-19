package vectors

type TestCaseHasBackdoor struct {
	In   string
	Want bool
}

type TestCasePart struct {
	Title string
	Want  int
}

var (
	CasesHasTLS = []TestCaseHasBackdoor{
		{"abba[mnop]qrst", true},
		{"abcd[bddb]xyyx", false},
		{"aaaa[qwer]tyui", false},
		{"ioxxoj[asdfgh]zxcvbn", true},
	}
	CasesHasSSL = []TestCaseHasBackdoor{
		{"aba[bab]xyz", true},
		{"xyx[xyx]xyx", false},
		{"aaa[kek]eke", true},
		{"zazbz[bzb]cdb", true},
	}
	CasesPart = map[int][]TestCasePart{
		1: {
			{"input", 105},
		},
		2: {
			{"input", 258},
		},
	}
)
