from enum import Enum
from dataclasses import dataclass
from typing import NewType, Tuple
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
class Point:
    x: int
    y: int

    def to_tuple(self) -> Tuple[int, int]:
        return self.x, self.y


class Clef(Enum):
    TREBLE = 0
    BASS = 1
