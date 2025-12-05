package testutil

import (
	"testing"
)

func MustPanic(t *testing.T, f func()) {
	t.Helper()
	defer func() {
		r := recover()
		if r == nil {
			t.Fatalf("panic expected, but did not happen")
		}
	}()
	f()
}
