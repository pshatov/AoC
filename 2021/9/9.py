# ---------------------------------------------------------------------------------------------------------------------
# AoC 2021
# ---------------------------------------------------------------------------------------------------------------------
# 9.py
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
# More Imports
# ---------------------------------------------------------------------------------------------------------------------
from PIL import Image, ImageDraw, ImageFont


# ---------------------------------------------------------------------------------------------------------------------
# Settings
# ---------------------------------------------------------------------------------------------------------------------
XY = 100

# noinspection SpellCheckingInspection
FONT_FILE = 'courbd.ttf'
FONT_SIZE = 20


# ---------------------------------------------------------------------------------------------------------------------
def create_field(f_lines):

    if len(f_lines) != XY or len(f_lines[0]) != XY:
        raise RuntimeError

    field = []
    for y in range(XY + 2):

        x = [10]
        if 0 < y <= XY:
            x += [int(t) for t in f_lines[y - 1]]
        else:
            x += [10] * XY
        x.append(10)

        field.append(x)

    return field
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def find_low_points(field):

    low_points = {}
    for y in range(XY):
        for x in range(XY):

            fxy = field[y + 1][x + 1]
            f_tp, f_bt = field[y][x + 1], field[y + 2][x + 1]
            f_lt, f_rt = field[y + 1][x], field[y + 1][x + 2]

            low = fxy < f_tp and fxy < f_bt and fxy < f_lt and fxy < f_rt

            if low:
                low_points[(x, y)] = fxy

    return low_points
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def create_image(field):

    palette = {}

    for v in range(10):
        palette[v] = 255 * (v + 1) // 10, 0, 0

    img = Image.new('RGB', (FONT_SIZE * XY, FONT_SIZE * XY))
    drw = ImageDraw.Draw(img)
    fnt = ImageFont.truetype(FONT_FILE, FONT_SIZE)

    for y in range(XY):
        for x in range(XY):
            t_value = field[y + 1][x + 1]
            t_string = str(t_value)
            t_color = palette[t_value]
            tx, ty = x * FONT_SIZE, y * FONT_SIZE
            t_width, t_height = fnt.getsize(t_string)
            dx, dy = (FONT_SIZE - t_width) // 2, (FONT_SIZE - t_height) // 2

            drw.text((tx + dx + 1, ty + dy - 1), t_string, t_color, font=fnt)

    return img, drw
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def find_basins(field, low_points, drw):

    border_clr = (191, 191, 191)
    center_clr = (255, 255, 0)

    basins = []
    for lp in low_points.keys():

        basins.append([])

        lpx0, lpy0 = lp[0] * FONT_SIZE, lp[1] * FONT_SIZE
        lpx1, lpy1 = lpx0 + FONT_SIZE, lpy0 + FONT_SIZE

        lpx0 += 1
        lpx1 -= 1
        lpy0 += 1
        lpy1 -= 1

        drw.line([(lpx0, lpy0), (lpx1, lpy0)], fill=center_clr, width=1)
        drw.line([(lpx0, lpy1), (lpx1, lpy1)], fill=center_clr, width=1)
        drw.line([(lpx0, lpy0), (lpx0, lpy1)], fill=center_clr, width=1)
        drw.line([(lpx1, lpy0), (lpx1, lpy1)], fill=center_clr, width=1)

        check_points = [lp]
        while len(check_points) > 0:

            next_check_points = []

            for cp in check_points:

                cpx, cpy = cp
                field[cpy + 1][cpx + 1] = -1

                cp_y_tp, cp_y_bt = cpy - 1, cpy + 1
                cp_x_lt, cp_x_rt = cpx - 1, cpx + 1

                cp_tp, cp_bt = field[cp_y_tp + 1][cpx + 1], field[cp_y_bt + 1][cpx + 1]
                cp_lt, cp_rt = field[cpy + 1][cp_x_lt + 1], field[cpy + 1][cp_x_rt + 1]

                if 0 <= cp_tp < 9 and (cpx, cp_y_tp) not in (check_points + next_check_points):
                    next_check_points.append((cpx, cpy - 1))
                if 0 <= cp_bt < 9 and (cpx, cp_y_bt) not in (check_points + next_check_points):
                    next_check_points.append((cpx, cpy + 1))
                if 0 <= cp_lt < 9 and (cp_x_lt, cpy) not in (check_points + next_check_points):
                    next_check_points.append((cpx - 1, cpy))
                if 0 <= cp_rt < 9 and (cp_x_rt, cpy) not in (check_points + next_check_points):
                    next_check_points.append((cpx + 1, cpy))

                x0, y0 = cpx * FONT_SIZE, cpy * FONT_SIZE
                x1, y1 = x0 + FONT_SIZE, y0 + FONT_SIZE

                if cp_tp == 9:
                    drw.line([(x0, y0), (x1, y0)], fill=border_clr, width=1)
                if cp_bt == 9:
                    drw.line([(x0, y1), (x1, y1)], fill=border_clr, width=1)

                if cp_lt == 9:
                    drw.line([(x0, y0), (x0, y1)], fill=border_clr, width=1)
                if cp_rt == 9:
                    drw.line([(x1, y0), (x1, y1)], fill=border_clr, width=1)

                basins[-1].append(cp)

            check_points = next_check_points

    return basins
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def main() -> None:

    with open('input.txt') as f:
        f_lines = [t.strip() for t in f.readlines()]

    field = create_field(f_lines)
    low_points = find_low_points(field)

    print("part 1: %d" % (sum(low_points.values()) + len(low_points)))

    img, drw = create_image(field)
    basins = find_basins(field, low_points, drw)
    basin_sizes = sorted([len(b) for b in basins])

    print("part 2: %d" % (basin_sizes[-1] * basin_sizes[-2] * basin_sizes[-3]))

    img.save('field.png')
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    main()
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
# End of File
# ---------------------------------------------------------------------------------------------------------------------
