import sys

from enum import Enum
from typing import Tuple, List, Optional, Dict


class RuleType(Enum):
    A = 'A'
    R = 'R'
    LT = '<'
    GT = '>'
    Z = 'Z'


class Rule:

    rule_type: RuleType
    category: Optional[str]
    rating: Optional[int]
    target: Optional[str]

    def __init__(self,
                 rule_type: RuleType,
                 category: Optional[str] = None,
                 rating: Optional[int] = None,
                 target: Optional[str] = None,
                 ) -> None:
        
        self.rule_type = rule_type

        if self.rule_type in [RuleType.LT, RuleType.GT]:
            self.category = category
            self.rating = rating
            self.target = target
        elif self.rule_type == RuleType.Z:
            self.target = target


class Part:

    x: int
    m: int
    a: int
    s: int

    def __repr__(self) -> str:
        return (f"x={self.x}"
                f", m={self.m}"
                f", a={self.a}"
                f", s={self.s}"
                )

    def __init__(self, line: str) -> None:
        assert line.startswith('{')
        assert line.endswith('}')

        line_parts = line[1 : -1].split(',')
        for index, next_part in enumerate(line_parts):
            part_left, part_right = next_part.split('=')
            if index == 0:
                assert part_left == "x"
                self.x = int(part_right)
            elif index == 1:
                assert part_left == "m"
                self.m = int(part_right)
            elif index == 2:
                assert part_left == "a"
                self.a = int(part_right)
            elif index == 3:
                assert part_left == "s"
                self.s = int(part_right)
            else:
                raise RuntimeError
            
    def rating(self, category: str) -> int:
        if category == "x":
            return self.x
        elif category == "m":
            return self.m
        elif category == "a":
            return self.a
        elif category == "s":
            return self.s
        else:
            raise RuntimeError


class Workflow:

    name: str
    rules: List[Rule]

    def __init__(self, line: str) -> None:

        assert line.endswith('}')

        self.name = ""
        while not line.startswith('{'):
            self.name += line[0]
            line = line[1:]

        self.rules = []
        line_parts = line[1 : -1].split(',')
        for next_part in line_parts:
            if '<' in next_part:
                a, bc = next_part.split('<')
                b, c = bc.split(':')
                self.rules.append(Rule(RuleType.LT,
                                       category=a,
                                       rating=int(b),
                                       target=c))
            elif '>' in next_part:
                a, bc = next_part.split('>')
                b, c = bc.split(':')
                self.rules.append(Rule(RuleType.GT,
                                       category=a,
                                       rating=int(b),
                                       target=c))
            elif next_part == RuleType.A.value:
                self.rules.append(Rule(RuleType.A))
            elif next_part == RuleType.R.value:
                self.rules.append(Rule(RuleType.R))
            else:
                self.rules.append(Rule(RuleType.Z,
                                       target=next_part))


def load_input(filename: str) -> Tuple[List[Part], List[Workflow]]:

    with open(filename) as f:
        lines = [l for l in [l.strip() for l in f] if l]

    workflows = []
    while not lines[0].startswith('{'):
        workflows.append(Workflow(lines.pop(0)))
    
    parts = []
    while len(lines) > 0:
        parts.append(Part(lines.pop(0)))
    
    return parts, workflows


def return_target(target: str) -> Tuple[str, int] | bool:
    if target == RuleType.A.value:
        return True
    elif target == RuleType.R.value:
        return False
    else:
        return target, 0
    

def step(part: Part,
         result: Tuple[str, int],
         workflows_lut: Dict[str, Workflow]) -> Tuple[str, int] | bool:

    workflow_name, rule_index = result
    workflow = workflows_lut[workflow_name]
    rule = workflow.rules[rule_index]

    if rule.rule_type == RuleType.LT:
        if part.rating(rule.category) < rule.rating:
            return return_target(rule.target)
        else:
            return workflow_name, rule_index + 1
    elif rule.rule_type == RuleType.GT:
        if part.rating(rule.category) > rule.rating:
            return return_target(rule.target)
        else:
            return workflow_name, rule_index + 1
    elif rule.rule_type == RuleType.Z:
        return rule.target, 0
    elif rule.rule_type == RuleType.A:
        return True
    elif rule.rule_type == RuleType.R:
        return False
    else:
        raise RuntimeError


def part1(filename: str) -> int:
    
    parts, workflows = load_input(filename)

    workflows_lut = {}
    for next_workflow in workflows:
        workflows_lut[next_workflow.name] = next_workflow

    a = []
    for next_part in parts:
        result = "in", 0
        while not isinstance(result, bool):
            result = step(next_part, result, workflows_lut)
        if result:
            a.append(next_part)

    total = 0
    for next_a in a:
        total += next_a.x
        total += next_a.m
        total += next_a.a
        total += next_a.s

    return total


def main() -> int:

    answer1 = part1('day_19_input.txt')
    print(f"{answer1}")

    # answer2 = part2(steps)
    # print(f"{answer2}")

    return 0


if __name__ == '__main__':
    sys.exit(main())
