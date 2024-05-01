import pytest

from day_01 import Day01


@pytest.fixture
def day01():
    def _day01(filename):
        return Day01(filename)
    return _day01


@pytest.fixture
def day01_sample1(day01):
    return day01('data/day_01_sample1.txt')


@pytest.fixture
def day01_sample2(day01):
    return day01('data/day_01_sample2.txt')


@pytest.fixture
def day01_input(day01):
    return day01('data/day_01_input.txt')


class TestDay01:
    
    def test_part1(self, day01_sample1, day01_input) -> None:
        assert day01_sample1.part1() == 142
        assert day01_input.part1() == 55834

    def test_part2(self, day01_sample2, day01_input) -> None:
        assert day01_sample2.part2() == 281
        assert day01_input.part2() == 53221
