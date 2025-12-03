package testutil

import (
	"os"
	"strings"
	"testing"
)

func readHelper(t *testing.T, file string) []string {
	t.Helper()

	data, err := os.ReadFile(file)
	if err != nil {
		t.Fatalf("failed to read '%s': %v", file, err)
	}

	lines := strings.Split(string(data), "\n")

	output := make([]string, 0, len(lines))
	for _, line := range lines {
		line = strings.TrimSpace(line)
		if line != "" {
			output = append(output, line)
		}
	}

	return output
}

func ReadAllLines(t *testing.T, file string) []string {
	t.Helper()
	return readHelper(t, file)
}

func ReadSingleLine(t *testing.T, file string) string {
	t.Helper()
	lines := readHelper(t, file)
	if len(lines) == 0 {
		t.Fatalf("empty file '%s'", file)
	} else if len(lines) > 1 {
		t.Fatalf("more than one line in file '%s'", file)
	}
	return lines[0]
}

func MustPanic(t *testing.T, f func()) {
	t.Helper()
	defer func() {
		r := recover()
		if r == nil {
			t.Fatalf("panic expected, but did not happen")
		}
	}()
	f()
}
