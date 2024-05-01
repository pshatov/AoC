from typing import List


class Day01:
  
    _SUBST = {'one':   1,
              'two':   2,
              'three': 3,
              'four':  4,
              'five':  5,
              'six':   6,
              'seven': 7,
              'eight': 8,
              'nine':  9}
    
    _input_lines: List[str]

    def __init__(self, filename: str) -> None:
        with open(filename) as f:
            self._input_lines = [l for l in [l.strip() for l in f] if l]

    @staticmethod
    def _get_first_digit(line: str) -> int:
        for ch in line:
            if str.isdigit(ch):
                return int(ch)
        else:
            raise RuntimeError

    @classmethod
    def _find_leftmost_digit(cls, line: str) -> int:
        for n in range(len(line)):
            part = line[:n+1]
            if str.isdigit(part[-1]):
                return int(part[-1])
            for digit in cls._SUBST:
                if part.endswith(digit):
                    return cls._SUBST[digit]

        raise RuntimeError

    @classmethod
    def _find_rightmost_digit(cls, line: str) -> int:
        for n in range(len(line)):
            part = line[-(n+1):]
            if str.isdigit(part[0]):
                return int(part[0])
            for digit in cls._SUBST:
                if part.startswith(digit):
                    return cls._SUBST[digit]
        
        raise RuntimeError

    def part1(self) -> int:
        total = 0
        for next_line in self._input_lines:
            a = self._get_first_digit(next_line)
            b = self._get_first_digit(reversed(next_line))
            total += 10 * a + b
        return total
    
    def part2(self) -> int:
        total = 0
        for next_line in self._input_lines:
            a = self._find_leftmost_digit(next_line)
            b = self._find_rightmost_digit(next_line)
            total += 10 * a + b
        return total
