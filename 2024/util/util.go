package util

import (
	"bufio"
	"fmt"
	"os"
)

func getFileName(parent string, day int, data string) string {
	return fmt.Sprintf("%s/data/day%02d_%s.txt", parent, day, data)
}

func LoadData(parent string, day int, data string) []string {
	fn := getFileName(parent, day, data)
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
