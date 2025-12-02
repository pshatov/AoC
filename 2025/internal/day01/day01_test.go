package day01

import (
	"aoc/2025/testutil"
	"testing"
)

func TestParseLine(t *testing.T) {
	type result struct {
		dir   int
		steps int
	}

	tests := []struct {
		title  string
		line   string
		wants  result
		panics bool
	}{
		{"left", "L2", result{-1, 2}, false},
		{"right", "R3", result{1, 3}, false},
		{"bad_dir", "X4", result{}, true},
		{"zero_steps", "L0", result{}, true},
		{"negative_steps", "R-1", result{}, true},
	}

	for _, tc := range tests {
		t.Run(tc.title, func(t *testing.T) {
			if tc.panics {
				testutil.MustPanic(t, func() {
					parseLine((tc.line))
				})
			} else {
				dir, steps := parseLine(tc.line)
				if dir != tc.wants.dir {
					t.Fatalf("parseLine(%s) dir = %d, but wants.dir = %d", tc.title, dir, tc.wants.dir)
				}
				if steps != tc.wants.steps {
					t.Fatalf("parseLine(%s) steps = %d, but wants.steps = %d", tc.title, steps, tc.wants.steps)
				}
			}
		})
	}
}

func TestUpdatePos(t *testing.T) {

	type result struct {
		newPos int
		final  int
		total  int
	}

	tests := []struct {
		title  string
		oldPos int
		dir    int
		steps  int
		wants  result
	}{
		{"no_overflow_right", 50, 1, 10, result{60, 0, 0}},
		{"no_overflow_left", 50, -1, 10, result{40, 0, 0}},

		{"just_before_wrap_right", 50, 1, 49, result{99, 0, 0}},
		{"precisely_wrap_right", 50, 1, 50, result{0, 1, 1}},
		{"right_after_wrap_right", 50, 1, 51, result{1, 0, 1}},

		{"just_before_wrap_left", 50, -1, 49, result{1, 0, 0}},
		{"precisely_wrap_left", 50, -1, 50, result{0, 1, 1}},
		{"right_after_wrap_left", 50, -1, 51, result{99, 0, 1}},

		{"full_loop_from_zero_right", 0, 1, numDials, result{0, 1, 1}},
		{"full_loop_from_zero_left", 0, -1, numDials, result{0, 1, 1}},

		{"full_loop_from_nonzero_right", 50, 1, numDials, result{50, 0, 1}},
		{"full_loop_from_nonzero_left", 50, -1, numDials, result{50, 0, 1}},
	}

	for _, tc := range tests {
		t.Run(tc.title, func(t *testing.T) {
			final, total := 0, 0
			newPos := updatePos(tc.oldPos, tc.dir, tc.steps, &final, &total)
			if newPos != tc.wants.newPos {
				t.Fatalf("updatePos(%s) newPos = %d, but wants.newPos = %d", tc.title, newPos, tc.wants.newPos)
			}
			if final != tc.wants.final {
				t.Fatalf("updatePos(%s) final = %d, but wants.final = %d", tc.title, final, tc.wants.final)
			}
			if total != tc.wants.total {
				t.Fatalf("updatePos(%s) total = %d, but wants.total = %d", tc.title, total, tc.wants.total)
			}
		})
	}
}

func TestCountZeroes(t *testing.T) {
	example := testutil.ReadLines(t, "example.txt")
	input := testutil.ReadLines(t, "input.txt")

	type result struct {
		final int
		total int
	}

	tests := []struct {
		title string
		lines []string
		wants result
	}{
		{"example", example, result{3, 6}},
		{"input", input, result{1102, 6175}},
	}

	for _, tc := range tests {
		t.Run(tc.title, func(t *testing.T) {
			final, total := CountZeroes(tc.lines)
			if final != tc.wants.final {
				t.Fatalf("CountZeroes(%s) final = %d, but wants.final = %d", tc.title, final, tc.wants.final)
			}
			if total != tc.wants.total {
				t.Fatalf("CountZeroes(%s) total = %d, but wants.total = %d", tc.title, total, tc.wants.total)
			}
		})
	}
}
