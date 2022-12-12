# ---------------------------------------------------------------------------------------------------------------------
# 12.py
# ---------------------------------------------------------------------------------------------------------------------
# AoC '22
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------------------------------------------------
import networkx as nx


# ---------------------------------------------------------------------------------------------------------------------
# More Imports
# ---------------------------------------------------------------------------------------------------------------------
from typing import List, Tuple, Optional


# ---------------------------------------------------------------------------------------------------------------------
def height2z(height: str) -> int:

    assert len(height) == 1

    height_lut = {'S': 'a',
                  'E': 'z'}

    if height in height_lut:
        height = height_lut[height]
    else:
        assert 'a' <= height <= 'z'

    return ord(height) - ord('a')
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
# noinspection PyPep8Naming
def add_edge(G: nx.classes.digraph.DiGraph,
             xy_src: Tuple[int, int],
             x_dst: int, y_dst: int, z_src: int,
             all_lines: List[str]) -> None:

    z_dst = height2z(all_lines[y_dst][x_dst])
    if z_dst <= z_src + 1:
        G.add_edge(xy_src, (x_dst, y_dst))
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def main() -> None:

    with open('input.txt') as file:
        all_lines = [line for line in [line.strip() for line in file] if line]

    # noinspection PyPep8Naming
    G = nx.DiGraph()

    dy = len(all_lines)
    dx = None
    for y in range(dy):
        next_line = all_lines[y]
        if y == 0:
            dx = len(next_line)
        else:
            assert len(next_line) == dx

    node_src, node_dst, nodes_lowest = None, None, []
    for y in range(dy):
        next_line = all_lines[y]
        for x in range(dx):
            xy = x, y
            height = next_line[x]
            z = height2z(height)
            if z == 0:
                nodes_lowest.append(xy)
            if height == 'S':
                node_src = xy
            elif height == 'E':
                node_dst = xy

            G.add_node(xy)

            if y > 0:
                add_edge(G, (x, y), x, y - 1, z, all_lines)
            if y < dy - 1:
                add_edge(G, (x, y), x, y + 1, z, all_lines)
            if x > 0:
                add_edge(G, (x, y), x - 1, y, z, all_lines)
            if x < dx - 1:
                add_edge(G, (x, y), x + 1, y, z, all_lines)

    path_nodes = nx.shortest_path(G, node_src, node_dst)
    print("part 1: %d" % (len(path_nodes) - 1))

    min_nodes: Optional[List]
    min_nodes = None
    for next_node in nodes_lowest:
        if nx.has_path(G, next_node, node_dst):
            path_nodes = nx.shortest_path(G, next_node, node_dst)
            if min_nodes is None or len(path_nodes) < len(min_nodes):
                min_nodes = path_nodes
    print("part 2: %d" % (len(min_nodes) - 1))
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    main()
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
# End of File
# ---------------------------------------------------------------------------------------------------------------------
