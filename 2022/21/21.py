# ---------------------------------------------------------------------------------------------------------------------
# 21.py
# ---------------------------------------------------------------------------------------------------------------------
# AoC '22
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
# More Imports
# ---------------------------------------------------------------------------------------------------------------------
from sympy import parse_expr, symbols, solve
from typing import Dict


# ---------------------------------------------------------------------------------------------------------------------
# Globals
# ---------------------------------------------------------------------------------------------------------------------
MonkeyLUT: Dict[str, str]
MonkeyLUT = {}


# ---------------------------------------------------------------------------------------------------------------------
def exec_num(parent_lut: Dict[str, str], parent_locals) -> None:
    exec_keys = []
    for m in parent_lut:
        if str.isnumeric(parent_lut[m]):
            line = "%s = %s" % (m, parent_lut[m])
            exec(line, None, parent_locals)
            exec_keys.append(m)
    for m in exec_keys:
        del parent_lut[m]
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def exec_sym(parent_lut: Dict[str, str], parent_locals) -> int:
    exec_keys = []
    for m in parent_lut:
        line = "%s = %s" % (m, parent_lut[m])
        try:
            exec(line, None, parent_locals)
        except NameError:
            continue
        exec_keys.append(m)
    for m in exec_keys:
        del parent_lut[m]
    return len(exec_keys)
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def run_part1() -> int:

    local_lut = MonkeyLUT.copy()

    exec_num(local_lut, locals())

    keep_yelling = True
    while keep_yelling:
        keep_yelling = exec_sym(local_lut, locals()) > 0

    assert 'root' in locals()

    return locals()['root']
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def run_part2() -> int:

    local_lut = MonkeyLUT.copy()

    root_parts = local_lut['root'].split(' ')
    assert len(root_parts) == 3
    root_one, root_two = root_parts[0], root_parts[2]
    del local_lut['root']

    assert str.isnumeric(local_lut['humn'])
    del local_lut['humn']

    exec_num(local_lut, locals())
    keep_yelling = True
    while keep_yelling:
        keep_yelling = exec_sym(local_lut, locals()) > 0

    if root_one in locals() and root_two not in locals():
        target_num, target_sym = locals()[root_one], root_two
    elif root_one not in locals() and root_two in locals():
        target_num, target_sym = locals()[root_two], root_one
    else:
        raise RuntimeError

    exec("%s = %d" % (target_sym, target_num))

    humn = symbols('humn')
    all_symbols = [humn]
    for m in local_lut:
        all_symbols.append(symbols(m))

    all_exprs = []
    for m in local_lut:
        line = "%s - %s" % (local_lut[m], m)
        expr = parse_expr(line.replace('//', '/'), locals())
        all_exprs.append(expr)

    result = solve(all_exprs, all_symbols)

    assert humn in result

    return result[humn]
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def main() -> None:

    with open('input.txt') as file:
        all_lines = [line for line in [line.strip() for line in file] if line]

    for next_line in all_lines:
        line_parts = next_line.replace('/', '//').split(': ')
        assert len(line_parts) == 2
        MonkeyLUT[line_parts[0]] = line_parts[1]

    part1 = run_part1()
    print("part 1: %d" % part1)

    part2 = run_part2()
    print("part 2: %d" % part2)
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    main()
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
# End of File
# ---------------------------------------------------------------------------------------------------------------------
