import sys

from typing import List


class GameResult:
    
    r: int
    g: int
    b: int

    def __init__(self, result: str) -> None:
        self.r, self.g, self.b = 0, 0, 0
        result_parts = result.split(',')
        for next_part in result_parts:
            if next_part.endswith('red'):
                self.r = int(next_part[:-3])
            elif next_part.endswith('green'):
                self.g = int(next_part[:-5])
            elif next_part.endswith('blue'):
                self.b = int(next_part[:-4])
            else:
                raise RuntimeError


class Game:

    index: int
    results: List[GameResult]

    def __init__(self, line: str) -> None:
        line = line.replace(' ', '')
        line_parts = line.split(':')
        assert len(line_parts) == 2
        game_index, game_results = line_parts

        assert game_index.startswith('Game')
        game_index = game_index[4:]
        self.index = int(game_index)

        self.results = []
        all_results = game_results.split(';')
        for next_result in all_results:
            self.results.append(GameResult(next_result))


def load_input(filename: str) -> List[Game]:

    with open(filename) as f:
        all_lines = [l for l in [l.strip() for l in f] if l]

    all_games = []
    for next_line in all_lines:
        all_games.append(Game(next_line))

    return all_games


def part1(filename: str, max_r: int, max_g: int, max_b: int) -> int:

    all_games = load_input(filename)

    sum = 0
    for next_game in all_games:
        for next_result in next_game.results:
            if next_result.r > max_r or\
                    next_result.g > max_g or\
                    next_result.b > max_b:
                break
        else:
            sum += next_game.index

    return sum


def part2(filename: str) -> int:

    all_games = load_input(filename)

    sum = 0
    for next_game in all_games:
        min_r = max(result.r for result in next_game.results)
        min_g = max(result.g for result in next_game.results)
        min_b = max(result.b for result in next_game.results)

        sum += min_r * min_g * min_b

    return sum


def main() -> int:

    max_r, max_g, max_b = 12, 13, 14

    sum1 = part1('day_02_input.txt', max_r, max_g, max_b)
    sum2 = part2('day_02_input.txt')

    print(f"{sum1}")
    print(f"{sum2}")

    return 0


if __name__ == '__main__':
    sys.exit(main())
