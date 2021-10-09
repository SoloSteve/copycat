import abc
import math
from enum import Enum
from typing import Any, Union
from abc import abstractmethod

from globals.global_types import Contour, Section

NOTE_ORDER = ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"]
WHITE_NOTES = ["A", "B", "C", "D", "E", "F", "G"]
BLACK_NOTES = ["A#", "C#", "D#", "F#", "G#"]
BLACK_NOTES_OFFSET_TABLE = [0, 1, 1, 2, 3, 3, 4]


class KeyColor(Enum):
    BLACK_KEY = 0
    WHITE_KEY = 1


class BasePianoKey(abc.ABC):
    @property
    @abstractmethod
    def note(self) -> str:
        pass

    @property
    @abstractmethod
    def section(self) -> Section:
        pass

    def __str__(self):
        return self.note

    def __repr__(self):
        return str(self)


class PianoKey(BasePianoKey):
    def __init__(self, absolute_index: int, section: Section):
        self.__index = absolute_index
        self.__section = section

    @property
    def note(self) -> str:
        letter = NOTE_ORDER[self.__index % len(NOTE_ORDER)]
        octave = (math.floor(self.__index / 12) + 1)
        return f"{letter}{octave}"

    @property
    def section(self) -> Section:
        return self.__section

    @staticmethod
    def note_to_index(note: str) -> int:
        letter = note[0:-1]
        octave = note[-1]

        return NOTE_ORDER.index(letter) + ((int(octave) - 1) * 12)


class PianoKeyContour(BasePianoKey):
    def __init__(self, contour: Contour, key_color: KeyColor, white_key_offset: int, local_index: int):
        self.__local_index = local_index
        self.__key_color = key_color
        self.__contour = contour
        self.__offset = white_key_offset

    @property
    def note(self) -> str:
        if self.__key_color == KeyColor.WHITE_KEY:
            real_index = self.__local_index + self.__offset
            letter = WHITE_NOTES[real_index % 7]
            octave = (math.floor(real_index / 7) + 1)
        else:
            real_index = self.__local_index + BLACK_NOTES_OFFSET_TABLE[self.__offset % 7]
            letter = BLACK_NOTES[real_index % 5]
            octave = (math.floor(real_index / 5) + math.floor(self.__offset / 7) + 1)
        return f"{letter}{octave}"

    @property
    def section(self) -> Any:
        return Section.from_contour(self.__contour)

    @staticmethod
    def note_to_index(note: str) -> int:
        letter = note[0:-1]
        octave = note[-1]

        if letter in WHITE_NOTES:
            index = WHITE_NOTES.index(letter) + (int(octave) - 1) * 7
        else:
            raise NotImplementedError("Only white keys are supported")
        return index
