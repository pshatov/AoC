package day05

import (
	"crypto/md5"
	"encoding/hex"
	"fmt"
	"io"
	"strconv"
	"strings"
)

func printState(door string, pwd []rune) {
	fmt.Printf("\r  %v: ", door)
	fmt.Printf("%v", string(pwd))
}

func hashChecker(door string) func() (string, bool) {
	index := -1
	worker := md5.New()
	return func() (string, bool) {
		index++
		worker.Reset()
		t := strconv.Itoa(index)
		io.WriteString(worker, door+t)
		hash := worker.Sum(nil)
		hex := hex.EncodeToString(hash)
		if strings.HasPrefix(hex, "00000") {
			return hex, true
		}
		return "", false
	}
}

func Part1(door string, silent bool) string {
	pwd := []rune("________")
	checker := hashChecker(door)
	if !silent {
		printState(door, pwd)
	}
	for j := 0; j < 8; j++ {
		for {
			hex, ok := checker()
			if ok {
				runes := []rune(hex)
				pwd[j] = runes[5]
				if !silent {
					printState(door, pwd)
				}
				break
			}
		}
	}
	return string(pwd)
}

func Part2(door string, silent bool) string {
	pwd := []rune("________")
	checker := hashChecker(door)
	if !silent {
		printState(door, pwd)
	}
	for j := 0; j < 8; j++ {
		for {
			hex, ok := checker()
			if ok {
				runes := []rune(hex)
				pos, err := strconv.Atoi(string(runes[5]))
				if err != nil || pos >= 8 || pwd[pos] != '_' {
					continue
				}
				pwd[pos] = runes[6]
				if !silent {
					printState(door, pwd)
				}
				break
			}
		}
	}
	return string(pwd)
}
