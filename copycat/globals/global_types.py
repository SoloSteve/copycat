from enum import Enum
from dataclasses import dataclass
from typing import NewType, Tuple

import cv2
from numpy import ndarray

Image = NewType("Image", ndarray)
Contour = NewType("Contour", ndarray)


@dataclass
class Bounds:
    x: int
    y: int
    width: int
    height: int


@dataclass
class Section:
    start: int
    end: int

    def size(self) -> int:
        return self.end - self.start

    @classmethod
    def from_contour(cls, contour: Contour):
        contour_x, _, contour_width, _ = cv2.boundingRect(contour)
        return cls(contour_x, contour_x + contour_width)


@dataclass
class Point:
    x: int
    y: int

    def to_tuple(self) -> Tuple[int, int]:
        return self.x, self.y


class Clef(Enum):
    TREBLE = 0
    BASS = 1
    NONE = 2
