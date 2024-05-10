package day03

type Triangle struct {
	A, B, C int
}

func IsValid(t *Triangle) bool {
	switch {
	case t.A+t.B <= t.C:
		return false
	case t.A+t.C <= t.B:
		return false
	case t.B+t.C <= t.A:
		return false
	}
	return true
}

func Part1(triangles []Triangle) int {
	n := 0
	for _, t := range triangles {
		if ok := IsValid(&t); ok {
			n++
		}
	}
	return n
}

func Part2(triangles []Triangle) int {
	count := len(triangles)
	if r := count % 3; r != 0 {
		panic("count is not a multiple of 3!")
	}

	n := 0
	for i := 0; i < len(triangles); i += 3 {
		t1 := Triangle{triangles[i].A, triangles[i+1].A, triangles[i+2].A}
		t2 := Triangle{triangles[i].B, triangles[i+1].B, triangles[i+2].B}
		t3 := Triangle{triangles[i].C, triangles[i+1].C, triangles[i+2].C}
		ok1 := IsValid(&t1)
		ok2 := IsValid(&t2)
		ok3 := IsValid(&t3)
		if ok1 {
			n++
		}
		if ok2 {
			n++
		}
		if ok3 {
			n++
		}
	}
	return n
}
