package vectors

type TestCase struct {
	Title, Want string
}

var (
	Cases = map[int][]TestCase{
		1: {
			{"example", "easter"},
			{"input", "agmwzecr"},
		},
		2: {
			{"example", "advent"},
			{"input", "owlaxqvq"},
		},
	}
)
