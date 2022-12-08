# ---------------------------------------------------------------------------------------------------------------------
# AoC 2015
# ---------------------------------------------------------------------------------------------------------------------
# 8.py
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
# More Imports
# ---------------------------------------------------------------------------------------------------------------------
from enum import Enum, auto


# ---------------------------------------------------------------------------------------------------------------------
class UnescapeState(Enum):
    AfterLiteral = auto()
    AfterEscape = auto()
    AfterHex0 = auto()
    AfterHex1 = auto()
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def unescape_line(line: str) -> str:

    hex_chars = "0123456789abcdef"

    assert line[0] == '"'
    line = line[1:]

    assert line[-1] == '"'
    line = line[:-1]

    new_line = ""
    escape_hex = None
    fsm = UnescapeState.AfterLiteral

    for s in line:

        if fsm == UnescapeState.AfterLiteral:
            if s != "\\":
                new_line += s
            else:
                fsm = UnescapeState.AfterEscape

        elif fsm == UnescapeState.AfterEscape:
            if s == "x":
                escape_hex = ""
                fsm = UnescapeState.AfterHex0
            elif s == "\"" or s == "\\":
                new_line += s
                fsm = UnescapeState.AfterLiteral
            else:
                raise RuntimeError

        elif fsm == UnescapeState.AfterHex0:
            assert s in hex_chars
            escape_hex += s
            fsm = UnescapeState.AfterHex1

        elif fsm == UnescapeState.AfterHex1:
            assert s in hex_chars
            escape_hex += s
            new_line += chr(int(escape_hex, 16))
            escape_hex = None
            fsm = UnescapeState.AfterLiteral
            
        else:
            raise RuntimeError

    return new_line
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def escape_line(line: str) -> str:

    new_line = ""
    for s in line:
        if s == "\\":
            new_line += "\\\\"
        elif s == "\"":
            new_line += "\\\""
        else:
            new_line += s

    new_line = "\"" + new_line + "\""

    return new_line
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def main() -> None:

    with open('input_8.txt') as file:
        all_lines = [line for line in [line.strip() for line in file.readlines()] if line]

    total_len_input = 0
    total_len_code = 0
    total_len_output = 0

    for input_line in all_lines:
        code_line = unescape_line(input_line)
        output_line = escape_line(input_line)

        print(f"{input_line} -> {code_line} -> {output_line}")

        total_len_input += len(input_line)
        total_len_code += len(code_line)
        total_len_output += len(output_line)

    print("part 1: %d" % (total_len_input - total_len_code))
    print("part 2: %d" % (total_len_output - total_len_input))
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    main()
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
# End-of-File
# ---------------------------------------------------------------------------------------------------------------------
