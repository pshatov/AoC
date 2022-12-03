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
def unescape_source_line(line: str) -> str:

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
def main() -> None:

    with open('input_8.txt') as file:
        all_lines = [line for line in [line.strip() for line in file.readlines()] if line]

    total_len_source = 0
    total_len_memory = 0
    for source_line in all_lines:

        total_len_source += len(source_line)

        memory_line = unescape_source_line(source_line)
        total_len_memory += len(memory_line)

    print("part 1: %d" % (total_len_source - total_len_memory))
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    main()
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
# End-of-File
# ---------------------------------------------------------------------------------------------------------------------
