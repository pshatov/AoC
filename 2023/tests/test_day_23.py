import pytest

from day_23 import Day23


@pytest.fixture
def day23():
    def _day23(filename):
        return Day23(filename)
    return _day23


@pytest.fixture
def day23_sample(day23):
    return day23('data/day_23_sample.txt')


class TestDay23:
    
    def test_part1(self, day23_sample) -> None:
        assert day23_sample.part1() == 94

    def test_part2(self, day01_sample2, day01_input) -> None:
        pass
