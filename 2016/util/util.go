package util

import (
	"fmt"
	"os"
	"strings"
	"testing"
)

func FormatDataPath(day int) string {
	return fmt.Sprintf("../data/day%02v.txt", day)
}

func LoadDataStrings(t *testing.T, fn string) []string {
	data, err := os.ReadFile(fn)
	if err != nil {
		t.Logf("Can't read %v", fn)
		t.FailNow()
	}

	result := []string{}
	lines := strings.Split(string(data), "\n")
	for _, ln := range lines {
		if t := len(ln); t > 0 {
			result = append(result, ln)
		}
	}

	return result
}
