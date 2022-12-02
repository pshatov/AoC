# ---------------------------------------------------------------------------------------------------------------------
# AoC 2015
# ---------------------------------------------------------------------------------------------------------------------
# 7.py
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
# More Imports
# ---------------------------------------------------------------------------------------------------------------------
from enum import Enum
from typing import List, Dict, Optional


# ---------------------------------------------------------------------------------------------------------------------
class CircuitType(Enum):
    Assign = ""
    Not = "NOT"
    And = "AND"
    Or = "OR"
    LShift = "LSHIFT"
    RShift = "RSHIFT"
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
class Circuit:

    ValueMask = 0xFFFF

    # -----------------------------------------------------------------------------------------------------------------
    def __init__(self, circuit_type: CircuitType, input_values: List[str], output_values: str) -> None:
        self.output_values = output_values
        self.circuit_type = circuit_type

        if self.circuit_type in CircuitShiftTypes:
            self.input_values = [input_values[0]]
            self.shift_param = int(input_values[1])
        else:
            self.input_values = input_values

        self.resolved = False
    # -----------------------------------------------------------------------------------------------------------------

    # -----------------------------------------------------------------------------------------------------------------
    def try_resolve(self) -> bool:

        assert not self.resolved

        all_inputs_resolved = True
        for v in self.input_values:
            if is_value_str(v) and Wires[v] is None:
                all_inputs_resolved = False
                break

        if not all_inputs_resolved:
            return False

        if self.circuit_type == CircuitType.Assign:
            value = self._resolve_input_value(self.input_values[0])

        elif self.circuit_type == CircuitType.Not:
            value = self._resolve_input_value(self.input_values[0])
            value ^= Circuit.ValueMask

        elif self.circuit_type == CircuitType.LShift:
            value = self._resolve_input_value(self.input_values[0])
            value <<= self.shift_param
            value &= Circuit.ValueMask

        elif self.circuit_type == CircuitType.RShift:
            value = self._resolve_input_value(self.input_values[0])
            value >>= self.shift_param

        elif self.circuit_type == CircuitType.Or:
            value_a = self._resolve_input_value(self.input_values[0])
            value_b = self._resolve_input_value(self.input_values[1])
            value = value_a | value_b

        elif self.circuit_type == CircuitType.And:
            value_a = self._resolve_input_value(self.input_values[0])
            value_b = self._resolve_input_value(self.input_values[1])
            value = value_a & value_b

        else:
            raise RuntimeError

        update_wire(self.output_values, value)
        self.resolved = True
        return True
    # -----------------------------------------------------------------------------------------------------------------

    # -----------------------------------------------------------------------------------------------------------------
    @staticmethod
    def _resolve_input_value(value: str) -> int:
        if is_value_int(value):
            return int(value)
        else:
            return int(Wires[value])
    # -----------------------------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
# Globals
# ---------------------------------------------------------------------------------------------------------------------
Wires: Dict[str, Optional[int]]
Circuits: List[Circuit]

Wires = {}
Circuits = []

CircuitShiftTypes = [CircuitType.LShift, CircuitType.RShift]


# ---------------------------------------------------------------------------------------------------------------------
def is_value_int(value: str) -> bool:
    return str.isdecimal(value)
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def is_value_str(value: str) -> bool:
    return not is_value_int(value)
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def update_wire(name: str, value: Optional[int] = None) -> None:

    assert is_value_str(name)

    if name not in Wires:
        Wires[name] = value
    else:
        assert Wires[name] is None
        Wires[name] = value
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def resolve_everything() -> None:

    keep_resolving = True
    while keep_resolving:

        num_resolved = 0
        for c in Circuits:
            if not c.resolved:
                ok = c.try_resolve()
                if ok:
                    num_resolved += 1

        keep_resolving = num_resolved > 0
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def main() -> None:

    with open('input_7.txt') as file:
        all_lines = [line for line in [line.strip() for line in file.readlines()] if line]

    for next_line in all_lines:

        line_src, line_dst = next_line.split(' -> ')

        assert is_value_str(line_dst)
        update_wire(line_dst)

        line_src_parts = line_src.split(' ')

        if len(line_src_parts) == 1:
            line_src = line_src_parts[0]
            if is_value_str(line_src):
                update_wire(line_src)
            Circuits.append(Circuit(CircuitType.Assign, [line_src], line_dst))

        elif len(line_src_parts) == 2:

            assert line_src_parts[0] == CircuitType.Not.value

            line_src = line_src_parts[1]
            if is_value_str(line_src):
                update_wire(line_src)

            Circuits.append(Circuit(CircuitType.Not, [line_src], line_dst))

        elif len(line_src_parts) == 3:

            line_src_x = line_src_parts[0]
            line_src_y = line_src_parts[2]

            circuit_type = CircuitType(line_src_parts[1])

            if is_value_str(line_src_x):
                update_wire(line_src_x)

            if circuit_type not in CircuitShiftTypes:
                if is_value_str(line_src_y):
                    update_wire(line_src_y)
            else:
                assert is_value_int(line_src_y)

            Circuits.append(Circuit(circuit_type, [line_src_x, line_src_y], line_dst))

        else:
            raise RuntimeError

    resolve_everything()
    print("part 1: %d" % Wires['a'])

    a_value = Wires['a']
    for w in Wires:
        Wires[w] = a_value if w == 'b' else None

    for c in Circuits:
        if c.output_values != 'b':
            c.resolved = False

    resolve_everything()
    print("part 2: %d" % Wires['a'])
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    main()
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
# End-of-File
# ---------------------------------------------------------------------------------------------------------------------
