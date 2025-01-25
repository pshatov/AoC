package main

import (
	"fmt"
	"os"
	"pshatov/aoc/year2024/day04"
	"pshatov/aoc/year2024/util"
)

func main() {
	if len(os.Args) != 2 {
		fmt.Println("USAGE: day04 <testcase>")
		os.Exit(1)
	}
	lines := util.LoadData("../..", day04.Day, os.Args[1])

	for _, finder := range []func(util.StringField) (int, util.ByteField){
		day04.FindXMASv1,
		day04.FindXMASv2,
	} {
		total, output := finder(lines)
		display := output.ToStringField()
		display.Print()
		fmt.Printf("    total = %d\n", total)
	}

	os.Exit(0)
}
