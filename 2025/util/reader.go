package util

import (
	"fmt"
	"os"
	"strings"
)

func readHelper(file string) []string {
	data, err := os.ReadFile(file)
	if err != nil {
		panic(fmt.Errorf("failed to read '%s': %w", file, err))
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

func ReadAllLines(file string) []string {
	return readHelper(file)
}

func ReadSingleLine(file string) string {
	lines := readHelper(file)
	if len(lines) == 0 {
		panic(fmt.Sprintf("empty file '%s'", file))
	} else if len(lines) > 1 {
		panic(fmt.Sprintf("more than one line in file '%s'", file))
	}
	return lines[0]
}
