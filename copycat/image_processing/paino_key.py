import math
from enum import Enum
from typing import Any

from global_types import Contour

NOTE_ORDER = ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"]
WHITE_NOTES = ["A", "B", "C", "D", "E", "F", "G"]
BLACK_NOTES = ["A#", "C#", "D#", "F#", "G#"]
BLACK_NOTES_OFFSET_TABLE = [0, 1, 1, 2, 3, 3, 4]


class ColorFamily(Enum):
    BLACK_KEY = 0
    WHITE_KEY = 1


class PianoKey:
    def __init__(self, contour: Contour, color_family: ColorFamily, white_key_offset: int, local_index: int):
        self.__local_index = local_index
        self.__color_family = color_family
        self.__contour = contour
        self.__offset = white_key_offset

    @property
    def note(self) -> str:
        if self.__color_family == ColorFamily.WHITE_KEY:
            real_index = self.__local_index + self.__offset
            letter = WHITE_NOTES[real_index % 7]
            octave = (math.floor(real_index / 7) + 1)
        else:
            real_index = self.__local_index + BLACK_NOTES_OFFSET_TABLE[self.__offset % 7]
            letter = BLACK_NOTES[real_index % 5]
            octave = (math.floor(real_index / 5) + math.floor(self.__offset / 7) + 1)
        return f"{letter}{octave}"

    @property
    def contour(self) -> Any:
        return self.__contour

    @staticmethod
    def note_to_index(note: str) -> int:
        letter = note[0:-1]
        octave = note[-1]

        if letter in WHITE_NOTES:
            index = WHITE_NOTES.index(letter) + (int(octave) - 1) * 7
        else:
            raise NotImplementedError("Only white keys are supported")
        return index

    def __str__(self):
        return self.note

    def __repr__(self):
        return str(self)
