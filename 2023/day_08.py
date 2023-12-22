import sys
import numpy as np

from typing import Tuple, List, Dict, Optional


class Node:

    name: str
    left: str
    right: str

    def __init__(self, name: str, left: str, right: str) -> None:
        self.name = name
        self.left = left
        self.right = right


Nodes = Dict[str, Node]


def load_input(filename: str) -> Tuple[str, Nodes]:

    with open(filename) as f:
        all_lines = [l for l in [l.strip() for l in f] if l]

    route = all_lines.pop(0)
    assert route.replace('R', '').replace('L', '') == ""

    all_nodes = {}
    for next_line in all_lines:

        node_from, nodes_to = tuple(next_line.replace(' ', '').split('='))

        assert node_from not in all_nodes
        assert nodes_to[0] == '(' and nodes_to[-1] == ')'

        node_to_left, node_to_right = tuple(nodes_to[1:-1].split(','))

        all_nodes[node_from] = Node(node_from, node_to_left, node_to_right)
        
    return route, all_nodes


def get_route_period(route: str,
                     all_nodes: List[Nodes],
                     node_from: str = 'AAA',
                     nodes_to: List[str] = ['ZZZ']):

    cnt = 0
    route_step = 0
    node = node_from
    while node not in nodes_to:
        if route[route_step] == "L":
            node = all_nodes[node].left
        elif route[route_step] == "R":
            node = all_nodes[node].right
        else:
            raise RuntimeError
        
        route_step += 1
        route_step %= len(route)

        cnt += 1

    return cnt



def part1(filename: str) -> Tuple[str, Nodes, int]:    
    route, all_nodes = load_input(filename)
    return route, all_nodes, get_route_period(route, all_nodes)


def part2(route: str, all_nodes: List[Node]) -> int:

    src_nodes = [n for n in all_nodes if n.endswith('A')]
    dst_nodes = [n for n in all_nodes if n.endswith('Z')]
    
    assert len(src_nodes) == len(dst_nodes)
    
    periods = []
    for i in range(len(src_nodes)):
        periods.append(get_route_period(route, all_nodes, src_nodes[i], dst_nodes))
    
    return np.lcm.reduce(periods)


def main() -> int:

    route, all_nodes, answer1 = part1('day_08_input.txt')
    answer2 = part2(route, all_nodes)

    print(f"{answer1}")
    print(f"{answer2}")

    return 0


if __name__ == '__main__':
    sys.exit(main())
