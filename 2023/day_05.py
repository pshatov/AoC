import sys
import networkx as nx

from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class Range:
    destination_start: int
    source_start: int
    range_length: int


@dataclass
class Map:
    source_category: str
    destination_category: str
    ranges: List[Range]


def load_input(filename: str) -> Tuple[List[int], List[Map]]:

    with open(filename) as f:
        all_lines = [l for l in [l.strip() for l in f] if l]

    header, seeds = tuple(t.strip() for t in all_lines[0].split(':'))
    assert header == "seeds"
    target_seeds = [int(t) for t in seeds.split(' ')]    

    del all_lines[0]

    all_maps: List[Map] = []
    while len(all_lines) > 0:
        direction, footer = tuple(t.strip() for t in all_lines[0].split(' '))
        assert footer == "map:"

        source, to, destination = tuple(direction.split('-'))
        assert to == "to"
        all_maps.append(Map(source, destination, []))
        del all_lines[0]

        while len(all_lines) > 0 and all_lines[0][0].isdigit():
            all_maps[-1].ranges.append(Range(*(int(t) for t in all_lines[0].split(' '))))
            del all_lines[0]

    return target_seeds, all_maps


def find_map(all_maps: List[Map], source: str, destination: str) -> Map:
    for next_map in all_maps:
        if next_map.source_category == source and next_map.destination_category == destination:
            return next_map
    raise RuntimeError


def apply_map(map: Map, value: int) -> int:
    for next_range in map.ranges:
        if value in range(next_range.source_start, next_range.source_start + next_range.range_length):
            return value - next_range.source_start + next_range.destination_start

    return value


def part1(filename: str) -> Tuple[List[int], List[Map], List[str], int]:
    target_seeds, all_maps = load_input(filename)

    g = nx.DiGraph()
    for next_map in all_maps:
        if next_map.source_category not in g.nodes:
            g.add_node(next_map.source_category)
        if next_map.destination_category not in g.nodes:
            g.add_node(next_map.destination_category)
        g.add_edge(next_map.source_category, next_map.destination_category)

    path = nx.shortest_path(g, 'seed', 'location')
    
    target_locations = []
    for next_target_seed in target_seeds:
        current_value = next_target_seed
        for i in range(1, len(path)):
            source, destination = path[i - 1 : i + 1]
            current_map = find_map(all_maps, source, destination)
            current_value = apply_map(current_map, current_value)
        target_locations.append(current_value)

    return target_seeds, all_maps, path, min(target_locations)



def part2(target_seeds: List[int], all_maps: List[Map], path: List[str]) -> int
    
    target_locations = []
    for next_target_seed in target_seeds:
        current_value = next_target_seed
        for i in range(1, len(path)):
            source, destination = path[i - 1 : i + 1]
            current_map = find_map(all_maps, source, destination)
            current_value = apply_map(current_map, current_value)
        target_locations.append(current_value)

    return target_seeds, all_maps, min(target_locations)


def main() -> int:

    target_seeds, all_maps, path, answer1 = part1('day_05_input.txt')
    answer2 = part2(target_seeds, all_maps, path)

    print(f"{answer1}")
    # print(f"{sum2}")

    return 0


if __name__ == '__main__':
    sys.exit(main())
