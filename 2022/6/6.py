# ---------------------------------------------------------------------------------------------------------------------
# 6.py
# ---------------------------------------------------------------------------------------------------------------------
# AoC '22
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def detect_pattern(signal: str, length: int) -> int:
    for i in range(length, len(signal) + 1):
        marker = signal[i - length: i]
        if len(set(marker)) == length:
            return i
    else:
        raise RuntimeError
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def main() -> None:

    with open('input.txt') as f:
        signal = f.readline().strip()

    print("part 1: %d" % detect_pattern(signal, 4))
    print("part 2: %d" % detect_pattern(signal, 14))
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    main()
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
# End of File
# ---------------------------------------------------------------------------------------------------------------------
