from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

from tqdm import tqdm

from notation.note_parser import NoteParser
from notation.note_stream import NoteStream, NoteInstance


class Notation:
    def __init__(self, fps: float, tempo: int, octave_offset: int):
        self._tempo = tempo
        self.note_parser = NoteParser(fps, tempo, octave_offset)

    def parse_stream(self, stream: NoteStream):
        song_frames: Dict[int, List[Tuple[NoteInstance, int]]] = defaultdict(list)
        notes: Dict[NoteInstance, NoteState] = defaultdict(NoteState)
        with tqdm(total=len(stream.stream) * 2, desc="creating abc notation...") as pbar:
            for i, frame in enumerate(stream.stream):
                pbar.update(1)
                for key in frame:
                    note_state = notes[key]
                    note_state.frame_count += 1
                    note_state.iteration = i
                for note, state in tuple(notes.items()):
                    if state.iteration != i:  # a note has ended
                        song_frames[state.iteration - state.frame_count].append((note, state.frame_count))
                        del notes[note]

            notation_string = ""
            rest_index: Optional[int] = None
            rest_clear = 0
            for i in range(len(stream.stream)):
                pbar.update(1)
                if len(notation_string) - notation_string.rfind("%") > 50:
                    notation_string += " %\n"
                if i in song_frames:
                    if rest_index is not None:
                        notation_string += f"{self.note_parser.get_rest_notation(i - rest_index)} "
                        rest_index = None

                    notes_notation = []
                    for notes_in_frame in song_frames[i]:
                        notes_notation.append(self.note_parser.get_notation(notes_in_frame[0], notes_in_frame[1]))
                        rest_clear = max(rest_clear, i + notes_in_frame[1])
                    notation_string += f"[{' '.join(notes_notation)}] "
                elif rest_index is None and i > rest_clear:
                    rest_index = i

        return notation_string

    def get_abc_notation(self, notation_string: str, title: str = "", composer: str = ""):
        return f"T: {title}\nC: {composer}\nQ: {self._tempo}\n{notation_string}"


@dataclass
class NoteState:
    frame_count: int = 0
    iteration: int = 0
