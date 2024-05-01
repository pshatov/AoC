import sys
import networkx as nx

from enum import Enum
from dataclasses import dataclass
from networkx import DiGraph
from typing import Tuple, Dict, List


class ModuleType(Enum):
    Simple = ''
    Flop = '%'
    Conj = '&'
    BCast = 'broadcaster'


@dataclass
class Signal:
    src: str
    dst: str
    value: bool


class Module:

    name: str
    module_type: ModuleType
    state: bool
    inputs: Dict[str, bool]
    outputs: List[str]
    
    def __init__(self, name: str) -> None:
        
        if name == ModuleType.BCast.value:
            self.module_type = ModuleType.BCast

        else:
            for mt in ModuleType:
                if name[0] == mt.value:
                    self.module_type = mt
                    name = name[1:]
                    break
            else:
                self.module_type = ModuleType.Simple

        self.name = name
        self.state = False
        self.inputs = dict()
        self.outputs = list()

    def __repr__(self) -> str:
        return self.name


Stats = {False: 0, True: 0}


def load_input(filename: str) -> Tuple[Dict[str, Module], DiGraph]:

    with open(filename) as f:
        all_lines = [l for l in [l.strip() for l in f] if l]

    modules: Dict[str, Module] = dict()
    graph = DiGraph()

    for next_line in all_lines:
        src, dests = next_line.split('->')
        
        src = src.strip()
        src_module = Module(src)
        if src_module.name not in graph.nodes:
            graph.add_node(src_module.name)
        modules[src_module.name] = src_module

        for dst in dests.split(','):
            dst = dst.strip()
            dst_module = Module(dst)
            if dst_module.name not in graph.nodes:
                graph.add_node(dst_module.name)
            graph.add_edge(src_module.name, dst_module.name)

    btn_module = Module('button')
    modules['button'] = btn_module
    graph.add_node(btn_module.name)
    graph.add_edge(btn_module.name, ModuleType.BCast.value)

    a = nx.nx_agraph.to_agraph(graph)
    a.layout(prog='dot')
    a.draw('a.png')

    for name in graph.nodes:

        if name not in modules:
            modules[name] = Module(name)

        for src, dst in graph.in_edges(name):
            assert dst == name
            modules[name].inputs[src] = False
        for src, dst in graph.out_edges(name):
            assert src == name
            modules[name].outputs.append(dst)

    return modules, graph


def propagate(modules: Dict[str, Module], signals: List[Signal]) -> List[Signal]:
    
    new_signals: List[Signal] = list()

    for s in signals:

        src = modules[s.src]
        dst = modules[s.dst]
        v = s.value

        if dst.name == "rx" and not v:
            print("!!!")

        #vs = "-high" if v else "-low"
        #print(f"{src.name} {vs}-> {dst.name}")

        if dst.module_type == ModuleType.BCast:
            for o in dst.outputs:
                new_signals.append(Signal(dst.name, o, v))
        elif dst.module_type == ModuleType.Flop:
            if v == False:
                dst.state = not dst.state
                for o in dst.outputs:
                    new_signals.append(Signal(dst.name, o, dst.state))
        elif dst.module_type == ModuleType.Conj:
            dst.inputs[src.name] = v
            for o in dst.outputs:
                new_signals.append(Signal(dst.name, o, not all(dst.inputs.values())))
        elif dst.module_type == ModuleType.Simple:
            pass
        else:
            raise RuntimeError

        Stats[v] += 1

    return new_signals


def part1(filename: str) -> Tuple[DiGraph, int]:
    
    modules, graph = load_input(filename)

    for n in range(1000000):
        signals = [Signal('button',
                          ModuleType.BCast.value,
                          False)]
        while len(signals) > 0:
            signals = propagate(modules, signals)

    total = Stats[False] * Stats[True]

    return modules, graph, total


# def part2(steps: List[str]) -> int:

#     lens_by_box: List[List[Lens]] = []
#     for i in range(256):
#         lens_by_box.append([])

#     for next_step in steps:
#         label = ""
#         for i in range(len(next_step)):
#             if not next_step[i].isalpha():
#                 break
#         label = next_step[:i]
#         box_index = aoc_hash(label)
#         op = next_step[i]
#         box = lens_by_box[box_index]
#         if op == '-':
#             remove_index = -1
#             for i, lens in enumerate(box):
#                 if lens.label == label:
#                     remove_index = i
#                     break
#             if remove_index != -1:
#                 del box[remove_index]
#         elif op == '=':
#             power = int(next_step[i + 1:])
#             replace_index = -1
#             for i, lens in enumerate(box):
#                 if lens.label == label:
#                     replace_index = i
#                     break
#             if replace_index != -1:
#                 box[replace_index] = Lens(label, power)
#             else:
#                 box.append(Lens(label, power))
#         else:
#             raise RuntimeError

#         if False:
#             print(f'After "{next_step}":')
#             for i, box in enumerate(lens_by_box):
#                 if len(box) > 0:
#                     print(f'Box {i}:', end='')
#                     for lens in box:
#                         print(f' [{lens.label} {lens.power}]', end='')
#                     print('\n')

#     total = 0
#     for i, box in enumerate(lens_by_box):
#         for j, lens in enumerate(box):
#             power = (i + 1) * (j + 1) * lens.power
#             total += power

#     return total


def main() -> int:

    modules, graph, answer1 = part1('day_20_input.txt')
    print(f"{answer1}")

    # answer2 = part2(steps)
    # print(f"{answer2}")

    return 0


if __name__ == '__main__':
    sys.exit(main())
