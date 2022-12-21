# ---------------------------------------------------------------------------------------------------------------------
# 16.py
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
from typing import List, Optional, Tuple


# ---------------------------------------------------------------------------------------------------------------------
# Globals
# ---------------------------------------------------------------------------------------------------------------------
ValveFlowLUT = {}
ValvePathLUT = {}
InitialNode = 'AA'


# ---------------------------------------------------------------------------------------------------------------------
def build_volcano(all_lines: List[str]) -> nx.DiGraph:

    volcano = nx.DiGraph()

    for next_line in all_lines:

        parts_valve = next_line.split(' ')
        assert len(parts_valve) > 2
        valve_name = parts_valve[1]

        parts_equal = next_line.split('=')
        assert len(parts_equal) == 2
        parts_flow = parts_equal[1].split(';')
        assert len(parts_flow) == 2
        flow_rate = int(parts_flow[0])

        parts_lead = next_line.split('lead')
        assert len(parts_lead) == 2
        while not parts_lead[1][0].isupper():
            parts_lead[1] = parts_lead[1][1:]
        parts_valves = parts_lead[1].replace(' ', '').split(',')

        if valve_name not in ValveFlowLUT:
            ValveFlowLUT[valve_name] = flow_rate
            volcano.add_node(valve_name)

        for next_valve in parts_valves:
            if next_valve not in volcano.nodes:
                volcano.add_node(next_valve)
            add_edge(volcano, valve_name, next_valve, 1)

    return volcano
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def add_edge(volcano: nx.DiGraph, node_a: str, node_b: str, weight: float) -> None:
    volcano.add_edge(node_a, node_b, weight=weight, label="%d" % weight)
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def add_valve_nodes(volcano: nx.DiGraph) -> None:
    active_valves = [v for v in ValveFlowLUT.keys() if ValveFlowLUT[v] > 0]
    for valve in active_valves:
        valve_handle = str.lower(valve)
        volcano.add_node(valve_handle)
        add_edge(volcano, valve, valve_handle, 1)
        add_edge(volcano, valve_handle, valve, 0)
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def plot_volcano(volcano: nx.DiGraph, filename: str) -> None:

    a = nx.nx_agraph.to_agraph(volcano)

    for e in a.edges_iter():
        del e.attr['weight']

    a.graph_attr['mode'] = "KK"
    a.graph_attr['scale'] = 1.5
    a.layout(prog='neato')

    a.draw(filename)
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def build_subpaths(volcano: nx.DiGraph,
                   current_path: List[str],
                   have_minutes: int,
                   valve_nodes: List[str]) -> List[List[str]]:

    potential_valves = [v for v in valve_nodes if v not in current_path]

    subpaths = []
    for pv in potential_valves:
        pv_cost = ValvePathLUT[current_path[-1]][pv]
        if pv_cost <= have_minutes:
            subpaths += build_subpaths(volcano, current_path + [pv], have_minutes - pv_cost, valve_nodes)

    return subpaths if len(subpaths) > 0 else [current_path]
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def calc_path_release(volcano: nx.DiGraph, path: List[str], time_limit: int) -> int:

    total_release = 0
    for i in range(1, len(path)):
        path_cost = ValvePathLUT[path[i - 1]][path[i]]
        total_release += ValveFlowLUT[str.upper(path[i])] * (time_limit - path_cost)
        time_limit -= path_cost

    assert time_limit >= 0

    return total_release
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def calc_max_dual_release(volcano: nx.DiGraph, all_paths: List[List[str]], time_limit: int) -> int:

    path_indices_by_release = {}
    for i in range(len(all_paths)):
        release = calc_path_release(volcano, all_paths[i], time_limit)
        if release not in path_indices_by_release:
            path_indices_by_release[release] = []
        path_indices_by_release[release].append(i)

    possible_single_release = list(path_indices_by_release.keys())
    paths_indices_by_dual_release = {}
    for i in range(len(possible_single_release)):
        for j in range(i, len(possible_single_release)):
            release_one = possible_single_release[i]
            release_two = possible_single_release[j]
            release_dual = release_one + release_two
            if release_dual not in paths_indices_by_dual_release:
                paths_indices_by_dual_release[release_dual] = []
            path_indices = path_indices_by_release[release_one], path_indices_by_release[release_two]
            paths_indices_by_dual_release[release_dual].append(path_indices)

    possible_dual_release = sorted(list(paths_indices_by_dual_release.keys()), reverse=True)
    for dual_release in possible_dual_release:
        path_indices = paths_indices_by_dual_release[dual_release]
        for path_indices_one, path_indices_two in path_indices:
            for i in path_indices_one:
                for j in path_indices_two:
                    set_one = set(all_paths[i][1:])
                    set_two = set(all_paths[j][1:])
                    set_common = set.intersection(set_one, set_two)
                    if len(set_common) == 0:
                        return dual_release
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def build_valve_path_lut(volcano: nx.DiGraph, valve_nodes: List[str]) -> None:
    for src in valve_nodes:
        ValvePathLUT[src] = {}
        for dst in valve_nodes:
            if src == dst:
                continue
            src_dst_path = nx.dijkstra_path(volcano, src, dst)
            ValvePathLUT[src][dst] = nx.path_weight(volcano, src_dst_path, 'weight')
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def main() -> None:

    with open('input.txt') as file:
        all_lines = [line for line in [line.strip() for line in file] if line]

    volcano = build_volcano(all_lines)
    assert len(ValveFlowLUT) == len(volcano.nodes)
    assert ValveFlowLUT[InitialNode] == 0

    add_valve_nodes(volcano)

    valve_nodes = [n for n in volcano.nodes if str.islower(n)]
    valve_nodes.append(InitialNode)

    build_valve_path_lut(volcano, valve_nodes)

    time_limit = 30
    all_paths = build_subpaths(volcano, [InitialNode], time_limit, valve_nodes)

    max_release = 0
    for next_path in all_paths:
        release = calc_path_release(volcano, next_path, time_limit)
        if release > max_release:
            max_release = release
    print("part 1: %d" % max_release)

    time_limit = 26
    all_paths = build_subpaths(volcano, [InitialNode], time_limit, valve_nodes)
    max_release = calc_max_dual_release(volcano, all_paths, time_limit)
    print("part 2: %d" % max_release)
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    main()
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
# End of File
# ---------------------------------------------------------------------------------------------------------------------
