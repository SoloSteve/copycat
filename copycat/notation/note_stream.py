from dataclasses import dataclass
from typing import List, Iterable

from tqdm import tqdm

from globallll.global_types import Clef, Image
from globallll.piano_key import BasePianoKey
from image_processing.note_press_detection import NoteDetector


def get_note_stream(frames: Iterable[Image],
                    total_frames: int,
                    keys: List[BasePianoKey],
                    detector: NoteDetector,
                    only_clef: Clef = Clef.NONE):
    note_stream = NoteStream()
    try:
        for frame in tqdm(frames, desc="Parsing video", total=total_frames):
            for key in keys:
                clef = detector.is_note_detected(key.section, frame)
                if clef is not Clef.NONE and (only_clef is None or clef == only_clef):
                    note_stream.push_note(NoteInstance.from_string(key.note, clef))
            note_stream.apply_frame()
    except Exception as e:
        raise
    return note_stream


@dataclass(eq=True, frozen=True)
class NoteInstance:
    letter: str
    is_sharp: bool
    octave: int
    clef: Clef

    @classmethod
    def from_string(cls, note_string: str, clef: Clef):
        return cls(letter=note_string[0], is_sharp=len(note_string) == 3, octave=int(note_string[-1]), clef=clef)

    def __str__(self):
        return f"{self.letter}{'#' if self.is_sharp else ''}{self.octave}"

    def __repr__(self):
        return str(self)


class NoteStream:
    def __init__(self):
        self.__stream: List[List[NoteInstance]] = []
        self.__current_frame_notes: List[NoteInstance] = []

    def push_note(self, note: NoteInstance):
        self.__current_frame_notes.append(note)

    def apply_frame(self):
        self.__stream.append(self.__current_frame_notes)
        self.__current_frame_notes = []

    @property
    def stream(self):
        return self.__stream