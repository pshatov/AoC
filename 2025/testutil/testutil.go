package testutil

import (
	"os"
	"strings"
	"testing"
)

func ReadLines(t *testing.T, file string) []string {
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
