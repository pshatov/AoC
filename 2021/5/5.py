# ---------------------------------------------------------------------------------------------------------------------
# AoC 2021
# ---------------------------------------------------------------------------------------------------------------------
# 5.py
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
# More Imports
# ---------------------------------------------------------------------------------------------------------------------
from PIL import Image
from typing import List, Tuple


# ---------------------------------------------------------------------------------------------------------------------
class LineClass:

    # -----------------------------------------------------------------------------------------------------------------
    def __init__(self, line: str) -> None:
        z = line.split(' -> ')
        self.x0, self.y0 = [int(z) for z in z[0].split(',')]
        self.x1, self.y1 = [int(z) for z in z[1].split(',')]
    # -----------------------------------------------------------------------------------------------------------------

    # -----------------------------------------------------------------------------------------------------------------
    @property
    def is_vertical(self):
        return self.x0 == self.x1
    # -----------------------------------------------------------------------------------------------------------------

    # -----------------------------------------------------------------------------------------------------------------
    @property
    def is_horizontal(self):
        return self.y0 == self.y1
    # -----------------------------------------------------------------------------------------------------------------

    # -----------------------------------------------------------------------------------------------------------------
    @property
    def xx_range(self):
        if self.x0 < self.x1:
            return range(self.x0, self.x1 + 1)
        else:
            return range(self.x0, self.x1 - 1, -1)
    # -----------------------------------------------------------------------------------------------------------------

    # -----------------------------------------------------------------------------------------------------------------
    @property
    def yy_range(self):
        if self.y0 < self.y1:
            return range(self.y0, self.y1 + 1)
        else:
            return range(self.y0, self.y1 - 1, -1)
    # -----------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
class FieldClass:

    HW = 1000
    IMG_COLOR_F = 51  # 255 / 5

    # -----------------------------------------------------------------------------------------------------------------
    def __init__(self, lines: List[LineClass]) -> None:

        self.lines = []
        for y in range(self.HW):
            self.lines.append([0] * self.HW)

        for ln in lines:

            if ln.is_horizontal:
                for x in ln.xx_range:
                    self.lines[ln.y0][x] += 1

            elif ln.is_vertical:
                for y in ln.yy_range:
                    self.lines[y][ln.x0] += 1

        self.img = Image.new('L', (self.HW, self.HW))
    # -----------------------------------------------------------------------------------------------------------------

    # -----------------------------------------------------------------------------------------------------------------
    @classmethod
    def min_max_x(cls, ln: LineClass) -> Tuple[int, int]:
        return cls._min_max_xy(ln.x0, ln.x1)
    # -----------------------------------------------------------------------------------------------------------------

    # -----------------------------------------------------------------------------------------------------------------
    @classmethod
    def min_max_y(cls, ln: LineClass) -> Tuple[int, int]:
        return cls._min_max_xy(ln.y0, ln.y1)
    # -----------------------------------------------------------------------------------------------------------------

    # -----------------------------------------------------------------------------------------------------------------
    @staticmethod
    def _min_max_xy(xy0: int, xy1: int) -> Tuple[int, int]:
        return min(xy0, xy1), max(xy0, xy1)
    # -----------------------------------------------------------------------------------------------------------------

    # -----------------------------------------------------------------------------------------------------------------
    @staticmethod
    def calc_min_max_xy(lines: List[LineClass]) -> None:

        xx = [ln.x0 for ln in lines] + [ln.x1 for ln in lines]
        yy = [ln.y0 for ln in lines] + [ln.y1 for ln in lines]

        x_min, x_max = min(xx), max(xx)
        y_min, y_max = min(yy), max(yy)

        print("x_min, x_max = %d, %d" % (x_min, x_max))
        print("y_min, y_max = %d, %d" % (y_min, y_max))
    # -----------------------------------------------------------------------------------------------------------------

    # -----------------------------------------------------------------------------------------------------------------
    def get_num_covers(self) -> int:

        num = 0
        for y in range(self.HW):
            for x in range(self.HW):
                if self.lines[y][x] > 1:
                    num += 1

        return num
    # -----------------------------------------------------------------------------------------------------------------

    # -----------------------------------------------------------------------------------------------------------------
    def count_diagonal(self, lines: List[LineClass]) -> None:

        for ln in lines:
            if not ln.is_horizontal and not ln.is_vertical:
                xx = iter(ln.xx_range)
                for y in ln.yy_range:
                    x = next(xx)
                    self.lines[y][x] += 1
    # -----------------------------------------------------------------------------------------------------------------

    # -----------------------------------------------------------------------------------------------------------------
    def calc_largest_cover_value(self):
        result = 0
        for y in range(self.HW):
            for x in range(self.HW):
                if self.lines[y][x] > result:
                    result = self.lines[y][x]

        return result
    # -----------------------------------------------------------------------------------------------------------------

    # -----------------------------------------------------------------------------------------------------------------
    def save_img(self, filename):
        for y in range(self.HW):
            for x in range(self.HW):
                self.img.putpixel((x, y), self.lines[y][x] * self.IMG_COLOR_F)

        self.img.save(filename)
    # -----------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def main() -> None:

    with open('input.txt') as f:
        f_lines = f.readlines()

    lines = []
    for fl in f_lines:
        lines.append(LineClass(fl.strip()))

    # FieldClass.calc_min_max_xy(lines)

    field = FieldClass(lines)
    print("part 1: num_covers = %s" % field.get_num_covers())
    field.save_img("field1.png")

    field.count_diagonal(lines)
    print("part 2: num_covers = %s" % field.get_num_covers())
    field.save_img("field2.png")

    # print("%d" % field.calc_largest_cover_value())
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    main()
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
# End of File
# ---------------------------------------------------------------------------------------------------------------------
