# ---------------------------------------------------------------------------------------------------------------------
# AoC 2021
# ---------------------------------------------------------------------------------------------------------------------
# 20.py
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
# More Imports
# ---------------------------------------------------------------------------------------------------------------------
from copy import deepcopy


# ---------------------------------------------------------------------------------------------------------------------
# More Imports
# ---------------------------------------------------------------------------------------------------------------------
from typing import List, Dict


# ---------------------------------------------------------------------------------------------------------------------
# New Types
# ---------------------------------------------------------------------------------------------------------------------
Trench = List[List[int]]


# ---------------------------------------------------------------------------------------------------------------------
def grow(img: Trench, img_buf: Trench) -> None:
    _grow_helper(img)
    _grow_helper(img_buf)
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def _grow_helper(img: Trench) -> None:

    n = len(img)

    for y in range(n):
        img[y].insert(0, 0)
        img[y].append(0)

    img.insert(0, [0] * (n + 2))
    img.append([0] * (n + 2))
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def partial_sum(img: Trench, x: int, y: int) -> int:

    s = 0

    s += img[y - 1][x - 1] * 2 ** 8
    s += img[y - 1][x] * 2 ** 7
    s += img[y - 1][x + 1] * 2 ** 6

    s += img[y][x - 1] * 2 ** 5
    s += img[y][x] * 2 ** 4
    s += img[y][x + 1] * 2 ** 3

    s += img[y + 1][x - 1] * 2 ** 2
    s += img[y + 1][x] * 2 ** 1
    s += img[y + 1][x + 1] * 2 ** 0

    return s
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def enhance(img: Trench, img_buf: Trench, enh: Dict[int, int]):

    # center of image
    ctr = len(img) // 2
    img_buf[ctr][ctr] = enh[partial_sum(img, ctr, ctr)]

    r = 1
    stop = False
    sss_ones = [False, False, False]
    sss_zeros = [False, False, False]
    filler = -1
    while not stop:

        yt, yb = ctr - r, ctr + r
        xl, xr = ctr - r, ctr + r

        s = 0
        for t in range(-r, r):
            a = enh[partial_sum(img, ctr + t, yt)]  # upper horizontal
            b = enh[partial_sum(img, ctr - t, yb)]  # lower horizontal
            c = enh[partial_sum(img, xl, ctr - t)]  # right vertical
            d = enh[partial_sum(img, xr, ctr + t)]  # left vertical

            img_buf[yt][ctr + t] = a
            img_buf[yb][ctr - t] = b
            img_buf[ctr - t][xl] = c
            img_buf[ctr + t][xr] = d

            s += (a + b + c + d)

        sss_ones.pop(0)
        sss_zeros.pop(0)
        sss_ones.append(s == 8 * r)
        sss_zeros.append(s == 0)

        r += 1

        stop = all(s for s in sss_ones) or all(s for s in sss_zeros)
        filler = img_buf[yt][xl]

    filled = False
    while not filled:

        yt, yb = ctr - r, ctr + r
        xl, xr = ctr - r, ctr + r

        for t in range(-r, r):
            img_buf[yt][ctr + t] = filler
            img_buf[yb][ctr - t] = filler
            img_buf[ctr - t][xl] = filler
            img_buf[ctr + t][xr] = filler

        r += 1
        filled = r > len(img_buf) // 2

    for y in range(len(img)):
        for x in range(len(img[y])):
            img[y][x] = img_buf[y][x]
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def draw(img: Trench) -> None:

    v_dict = {0: '.',
              1: '#'}

    for y_img in img:
        for v in y_img:
            print(v_dict[v], end='')
        print()
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def main() -> None:

    with open('input.txt') as f:
        f_lines = [t.strip() for t in f.readlines()]

    # store algorithm
    img_enh_alg = f_lines[0]
    assert len(img_enh_alg) == 512

    # store image
    img = []
    for fl in f_lines[1:]:
        if not fl:
            continue
        img.append([0 if c == '.' else 1 for c in fl])

    # craft dictionary
    img_enh_dict = {}
    for i in range(len(img_enh_alg)):
        img_enh_dict[i] = 0 if img_enh_alg[i] == '.' else 1

    # make width odd (if needed)
    for y in range(len(img)):
        if len(img[y]) % 2 == 0:
            img[y].append(0)

    # make height odd (if needed)
    if len(img) % 2 == 0:
        img.append([0] * len(img[0]))

    img_buf = deepcopy(img)

    for i in range(2):
        for j in range(10):
            grow(img, img_buf)
        enhance(img, img_buf, img_enh_dict)
    # draw(img)

    s = sum(sum(img_y) for img_y in img)
    print("part 1: %d" % s)

    for i in range(50 - 2):
        for j in range(10):
            grow(img, img_buf)
        enhance(img, img_buf, img_enh_dict)
    # draw(img)

    s = sum(sum(img_y) for img_y in img)
    print("part 2: %d" % s)
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    main()
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
# End of File
# ---------------------------------------------------------------------------------------------------------------------
