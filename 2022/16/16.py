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

from packaging._manylinux import _parse_glibc_version

# ---------------------------------------------------------------------------------------------------------------------
# Globals
# ---------------------------------------------------------------------------------------------------------------------
ValveFlowLUT = {}
InitialValve = 'AA'


# ---------------------------------------------------------------------------------------------------------------------
def find_all_subpaths(volcano: nx.DiGraph, limit: float, current_path: List[str]) -> List[List[str]]:

    if nx.path_weight(volcano, current_path, weight='weight') > limit:
        return [current_path[:-1]]
    elif nx.path_weight(volcano, current_path, weight='weight') == limit:
        return [current_path]

    new_paths = []
    all_neighbors = volcano.neighbors(current_path[-1])
    for next_neighbor in all_neighbors:

        if node_is_valve(next_neighbor):
            if next_neighbor in current_path:
                continue
            if ValveFlowLUT[next_neighbor] == 0:
                continue
        else:

            if len(current_path) > 1:
                discard_path = False
                for i in range(len(current_path) - 1, -1, -1):
                    if current_path[i] == next_neighbor:
                        discard_path = True
                        break
                    if i < (len(current_path) - 1) and volcano.has_edge(current_path[i], next_neighbor):
                        discard_path = True
                        break
                    if node_is_valve(current_path[i]):
                        break
                if discard_path:
                    continue

        new_paths += find_all_subpaths(volcano, limit, current_path + [next_neighbor])

    return new_paths
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def calc_path_release(volcano: nx.DiGraph, path: List[str]) -> int:

    assert path[0] == InitialValve

    t0 = 0.0
    total_release, open_valves, pending_valve = 0, [], None
    valve_just_opened = None
    for i in range(1, len(path)):

        next_node = path[i]
        t = nx.path_weight(volcano, path[0 : i + 1], weight='weight')

        if node_is_valve(next_node):
            while t - t0 > 0.75:
                for next_valve in open_valves:
                    if next_valve in ValveFlowLUT:
                        total_release += ValveFlowLUT[next_valve]
                    else:
                        total_release += ValveFlowLUT[str.upper(next_valve)]
                t0 += 1.0
            pending_valve = next_node
            valve_just_opened = True

        else:
            while t - t0 > 0.75:
                for next_valve in open_valves:
                    if next_valve in ValveFlowLUT:
                        total_release += ValveFlowLUT[next_valve]
                    else:
                        total_release += ValveFlowLUT[str.upper(next_valve)]
                t0 += 1.0

            if valve_just_opened:
                open_valves.append(pending_valve)
                pending_valve = None

            valve_just_opened = False
    return total_release
# ---------------------------------------------------------------------------------------------------------------------


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
            add_edge(volcano, valve_name, next_valve, 1.0)

    return volcano
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def add_edge(volcano: nx.DiGraph, node_a: str, node_b: str, weight: float) -> None:
    volcano.add_edge(node_a, node_b, weight=weight, label="%.1f" % weight)
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def add_valve_nodes(volcano: nx.DiGraph) -> None:
    active_valves = [v for v in ValveFlowLUT.keys() if ValveFlowLUT[v] > 0]
    for valve in active_valves:
        valve_handle = str.lower(valve)
        ValveFlowLUT[valve_handle] = ValveFlowLUT[valve]
        volcano.add_node(valve_handle)
        add_edge(volcano, valve, valve_handle, 0.5)
        add_edge(volcano, valve_handle, valve, 0.5)
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
def find_nodes_to_contract(volcano: nx.DiGraph) -> Optional[Tuple[str, str]]:

    all_nodes = list(volcano.nodes)

    for i in range(len(all_nodes)):
        node_a = all_nodes[i]
        if node_is_valve(node_a) or node_a == InitialValve:
            continue

        for j in range(i + 1, len(all_nodes)):
            node_b = all_nodes[j]
            if node_is_valve(node_b) or node_b == InitialValve:
                continue

            if ValveFlowLUT[node_a] == 0 and ValveFlowLUT[node_b] == 0:
                if volcano.has_edge(node_a, node_b) and volcano.has_edge(node_b, node_a):
                    return node_a, node_b

    return None
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def find_valve_to_contract(volcano: nx.DiGraph) -> Optional[Tuple[str, str, str]]:

    all_nodes = list(volcano.nodes)

    for i in range(len(all_nodes)):
        node_valve = all_nodes[i]

        if not node_is_valve(node_valve):
            continue

        parent_node = list(volcano.neighbors(node_valve))
        if len(parent_node) != 1:
            continue
        parent_node = parent_node[0]

        near_nodes = [node for node in volcano.neighbors(parent_node) if node != node_valve]
        if len(near_nodes) != 1:
            continue
        near_node = near_nodes[0]

        return near_node, parent_node, node_valve

    return None
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def contract_in_edges(volcano: nx.DiGraph, volcano_new: nx.DiGraph, node_a: str, node_b: str, node_ab: str) -> None:
    for node_from, _ in volcano.in_edges(node_a):
        if node_from != node_b:
            add_edge(volcano_new, node_from, node_ab, weight=volcano[node_from][node_a]['weight'])
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def contract_out_edges(volcano: nx.DiGraph, volcano_new: nx.DiGraph, node_a: str, node_b: str, node_ab: str) -> None:
    for _, node_to in volcano.out_edges(node_a):
        if node_to != node_b:
            add_edge(volcano_new, node_ab, node_to, weight=volcano[node_a][node_to]['weight'] + 1.0)
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def do_contract_nodes(volcano: nx.DiGraph, contract_nodes: Tuple[str, str]) -> nx.DiGraph:

    volcano_new = volcano.copy()

    node_a, node_b = contract_nodes
    node_ab = node_a + node_b

    del ValveFlowLUT[node_a]
    del ValveFlowLUT[node_b]

    ValveFlowLUT[node_ab] = 0

    volcano_new.remove_node(node_a)
    volcano_new.remove_node(node_b)
    volcano_new.add_node(node_ab)

    contract_in_edges(volcano, volcano_new, node_a, node_b, node_ab)
    contract_in_edges(volcano, volcano_new, node_b, node_a, node_ab)

    contract_out_edges(volcano, volcano_new, node_a, node_b, node_ab)
    contract_out_edges(volcano, volcano_new, node_b, node_a, node_ab)

    return volcano_new
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def contract_in_valves(volcano: nx.DiGraph, volcano_new: nx.DiGraph,
                       node_near: str, node_parent: str, node_valve: str, node_contracted: str) -> None:
    for node_from, _ in volcano.in_edges(node_near):
        if node_from != node_parent:
            weight = volcano[node_from][node_near]['weight'] +\
                volcano[node_near][node_parent]['weight'] +\
                volcano[node_parent][node_valve]['weight']
            add_edge(volcano_new, node_from, node_contracted, weight=weight)
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def contract_out_valves(volcano: nx.DiGraph, volcano_new: nx.DiGraph,
                        node_near: str, node_parent: str, node_valve: str, node_contracted: str) -> None:
    for _, node_to in volcano.out_edges(node_near):
        if node_to != node_parent:
            weight = volcano[node_near][node_to]['weight'] +\
                volcano[node_parent][node_near]['weight'] +\
                volcano[node_valve][node_parent]['weight']
            add_edge(volcano_new, node_contracted, node_to, weight=weight)
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def do_contract_valve(volcano: nx.DiGraph, contract_valve: Tuple[str, str, str]) -> nx.DiGraph:

    volcano_new = volcano.copy()

    node_near, node_parent, node_valve = contract_valve
    node_contracted = node_near + node_parent + node_valve

    ValveFlowLUT[node_contracted] = ValveFlowLUT[node_parent]

    del ValveFlowLUT[node_near]
    del ValveFlowLUT[node_parent]

    volcano_new.remove_node(node_near)
    volcano_new.remove_node(node_parent)
    volcano_new.remove_node(node_valve)
    volcano_new.add_node(node_contracted)

    contract_in_valves(volcano, volcano_new, node_near, node_parent, node_valve, node_contracted)
    contract_out_valves(volcano, volcano_new, node_near, node_parent, node_valve, node_contracted)

    return volcano_new
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def contract_volcano(volcano: nx.DiGraph) -> nx.DiGraph:

    keep_contracting = True
    while keep_contracting:

        keep_contracting = False
        contract_nodes = find_nodes_to_contract(volcano)

        if contract_nodes is not None:
            volcano = do_contract_nodes(volcano, contract_nodes)
            keep_contracting = True

    return volcano
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def contract_valves(volcano: nx.DiGraph) -> nx.DiGraph:

    num_contracted = 0
    keep_contracting = True
    while keep_contracting:

        keep_contracting = False
        contract_valve = find_valve_to_contract(volcano)

        if contract_valve is not None:
            volcano = do_contract_valve(volcano, contract_valve)
            num_contracted += 1
            plot_volcano(volcano, 'volcano_valves_%d.png' % num_contracted)
            keep_contracting = True

    return volcano
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def node_is_valve(node: str) -> bool:
    return str.islower(node[-2:])
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def main() -> None:

    with open('input.txt') as file:
        all_lines = [line for line in [line.strip() for line in file] if line]

    volcano = build_volcano(all_lines)
    assert len(ValveFlowLUT) == len(volcano.nodes)
    assert ValveFlowLUT[InitialValve] == 0

    add_valve_nodes(volcano)

    num_valves = 0
    for n in volcano.nodes:
        if node_is_valve(n) and ValveFlowLUT[n] > 0:
            num_valves += 1
    print("num_valves: %d" % num_valves)

    s = 1
    for i in range(num_valves, 0, -1):
        s *= i
    print("s = %d" % s)

    return

    volcano_original = volcano.copy()
    plot_volcano(volcano_original, 'volcano_original.png')

    volcano = contract_volcano(volcano)
    plot_volcano(volcano, 'volcano_contracted.png')
    volcano = contract_valves(volcano)
    plot_volcano(volcano, 'volcano_final.png')

    # total_minutes = 30
    for i in range(2, 30):
        all_paths = find_all_subpaths(volcano, float(i), [InitialValve])
        if i == 29:
            for p in all_paths:
                print(p)
        print("%d: %d" % (i, len(all_paths)))
    #
    # paths_releases = []
    # for next_path in all_paths:
    #     release = calc_path_release(volcano, next_path)
    #     paths_releases.append(release)
    #
    # print("part 1: %d" % max(paths_releases))
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    main()
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
# End of File
# ---------------------------------------------------------------------------------------------------------------------
