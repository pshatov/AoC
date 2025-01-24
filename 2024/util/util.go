package util

import (
	"bufio"
	"fmt"
	"os"
)

func getFileName(day int, data string) string {
	return fmt.Sprintf("../data/day%02d_%s.txt", day, data)
}

func LoadData(day int, data string) []string {
	fn := getFileName(day, data)
	file, err := os.Open(fn)
	if err != nil {
		panic(fmt.Errorf("can't read data file '%s'", fn))
	}
	defer file.Close()
	var lines []string
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		lines = append(lines, scanner.Text())
	}
	return lines
}
