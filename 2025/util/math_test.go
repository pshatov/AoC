package util

import "testing"

func TestAbsInt(t *testing.T) {
	tests := []struct {
		x, wants int
	}{
		{1, 1},
		{2, 2},
		{3, 3},
		{0, 0},
		{-1, 1},
		{-2, 2},
		{-3, 3},
	}
	for _, tc := range tests {
		result := AbsInt(tc.x)
		if result != tc.wants {
			t.Fatalf("absInt(%d) failed, result = %d, but wants = %d",
				tc.x, result, tc.wants)
		}
	}
}

func TestMinInt(t *testing.T) {
	tests := []struct {
		x, y, wants int
	}{
		{2, 3, 2},
		{3, 2, 2},
		{2, 2, 2},
	}
	for _, tc := range tests {
		result := MinInt(tc.x, tc.y)
		if result != tc.wants {
			t.Fatalf("minInt(%d, %d) failed, result = %d, but wants = %d",
				tc.x, tc.y, result, tc.wants)
		}
	}
}

func TestMaxInt(t *testing.T) {
	tests := []struct {
		x, y, wants int
	}{
		{2, 3, 3},
		{3, 2, 3},
		{3, 3, 3},
	}
	for _, tc := range tests {
		result := MaxInt(tc.x, tc.y)
		if result != tc.wants {
			t.Fatalf("maxInt(%d, %d) failed, result = %d, but wants = %d",
				tc.x, tc.y, result, tc.wants)
		}
	}
}
