import numpy as np

from globals.color import Color
from globals.global_types import Image, Clef, Section

BLUE = Color(b=255, g=0, r=0)
GREEN = Color(b=0, g=255, r=0)


class NoteDetector:
    def __init__(self, control_frame: Image, detection_height: int, detection_threshold: float):
        self._detection_height = detection_height
        self._detection_threshold = detection_threshold
        self._control_detection_line = control_frame[detection_height]

    def is_note_detected(self, section: Section, image: Image) -> Clef:
        control_color = _get_mean_color_at_slice(self._control_detection_line[section.start: section.end])

        checked_color = _get_mean_color_at_slice(image[self._detection_height][section.start: section.end])
        if control_color.diff(checked_color) <= self._detection_threshold:
            return Clef.NONE

        return Clef.BASS if checked_color.closer_to(BLUE, GREEN) == BLUE else Clef.TREBLE


def _get_mean_color_at_slice(color_slice: np.ndarray) -> Color:
    return Color.from_bgr(*color_slice.mean(axis=0))
