package util

type ByteField [][]byte

func (b ByteField) Dx() int {
	return len(b[0])
}

func (b ByteField) Dy() int {
	return len(b)
}

func (b ByteField) Fill(ch byte) {
	for y := 0; y < b.Dy(); y++ {
		for x := 0; x < b.Dx(); x++ {
			b[y][x] = ch
		}
	}
}

func (b ByteField) ToStringField() StringField {
	var f []string
	for _, ln := range b {
		f = append(f, string(ln))
	}
	return f
}

func (b ByteField) Copy() ByteField {
	var c [][]byte
	for i, ln := range b {
		c = append(c, make([]byte, len(ln)))
		copy(c[i], ln)
	}
	return c
}
