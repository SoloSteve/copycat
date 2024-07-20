from globallll.math_utils import take_closest
from notation.consts import LENGTHS, OCTAVES
from notation.note_stream import NoteInstance


class NoteParser:
    def __init__(self, fps: float, tempo: int, octave_offset: int):
        self._fps = fps
        self._tempo = tempo
        self._offset = octave_offset

    def get_notation(self, note: NoteInstance, frame_count: int) -> str:
        note_notation = NoteParser.octave_parser(note.letter, note.octave)
        if note.is_sharp:
            note_notation = f"^{note_notation}"
        beat_length = NoteParser.round_beat_length(NoteParser.get_beat_count(frame_count, self._fps, self._tempo))
        note_notation = f"{note_notation}{LENGTHS[beat_length]}"
        return note_notation

    def get_rest_notation(self, frame_count: int) -> str:
        beat_length = NoteParser.round_beat_length(NoteParser.get_beat_count(frame_count, self._fps, self._tempo))
        rest_notation = f"z{LENGTHS[beat_length]}"
        return rest_notation

    @staticmethod
    def get_beat_count(frame_count: int, fps: float, tempo: int):
        held_seconds = frame_count / fps
        beat_length_in_seconds = 60 / tempo  # quarter note
        beat_count = round(held_seconds / beat_length_in_seconds, 2)
        return beat_count

    @staticmethod
    def round_beat_length(beat_count: float):
        lengths = list(LENGTHS.keys())
        return lengths[take_closest(lengths, beat_count)]

    @staticmethod
    def octave_parser(letter: str, octave: int) -> str:
        return OCTAVES[f"{letter}{octave}"]