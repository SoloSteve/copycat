from math import sqrt


class Color:
    """
    Represents a color made of red green and blue.
    This class is used for color calculation.
    """

    def __init__(self, b, g, r):
        self.r = int(r)
        self.g = int(g)
        self.b = int(b)

    def diff(self, other):
        """
        Between 0 and 1

        https://en.wikipedia.org/wiki/Color_difference
        """
        return sqrt(
            (self.r - other.r) ** 2 + (self.g - other.g) ** 2 + (self.b - other.b) ** 2
        ) / sqrt(
            255 ** 2 + 255 ** 2 + 255 ** 2
        )

    def __eq__(self, other):
        return self.r == other.r and self.g == other.g and self.b == other.b

    def __gt__(self, other):
        return self - other > 0

    def __lt__(self, other):
        return self - other < 0

    def __sub__(self, other):
        return sqrt(self.r ** 2 + self.g ** 2 + self.b ** 2) - sqrt(other.r ** 2 + other.g ** 2 + other.b ** 2)

    def __str__(self):
        return f"{self.r},{self.g},{self.b}"

    def to_tuple(self):
        return self.b, self.g, self.r

    def closer_to(self, other1, other2):
        if self.diff(other1) < self.diff(other2):
            return other1
        else:
            return other2

    @staticmethod
    def from_bgr(b: int, g: int, r: int):
        return Color(b=b, g=g, r=r)

    @staticmethod
    def from_rbg(r: int, b: int, g: int):
        return Color(b=b, g=g, r=r)
