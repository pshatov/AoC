package util

import (
	"errors"
	"fmt"
)

type StringField []string

func (s StringField) ToByteField() ByteField {
	var bf ByteField
	var dx, dy int
	for i, ln := range s {
		if i == 0 {
			dx = len(ln)
		} else if len(ln) != dx {
			panic(fmt.Errorf(
				"can't convert to binary field: the first line is %d bytes, line #%d is %d bytes",
				dx, i+1, len(ln)))
		}
		dy++
		bf = append(bf, []byte(ln))
	}
	if dy == 0 {
		panic(errors.New("can't convert to binary field: no lines"))
	}
	return bf
}

func (s StringField) Print() {
	for _, ln := range s {
		fmt.Printf("    %s\n", ln)
	}
}
