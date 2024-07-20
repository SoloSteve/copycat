from typing import List, Tuple

import numpy as np

from globals.color import Color
from globals.global_types import Image, Section
from globals.paino_key import PianoKey, KeyColor
from image_processing.image_manipulations import reduce_colors

WHITE = Color(255, 255, 255)
BLACK = Color(0, 0, 0)


def get_piano_keys(control_frame: Image, key_offset: int, detection_height: int) -> List[PianoKey]:
    binary_keyboard = reduce_colors(control_frame, 2)
    detection_line = binary_keyboard[detection_height]

    sections = _get_sections_by_border_detection(detection_line)
    sections = [Section(x[0], x[1]) for x in sections]
    sections = _filter_noise(sections, 5)

    piano_keys = []

    for i, section in enumerate(sections):
        piano_keys.append(
            PianoKey(
                absolute_index=i + key_offset,
                section=section
            )
        )
    return piano_keys


def _get_sections_by_border_detection(detection_line: np.ndarray) -> List[Tuple[int, int]]:
    sections = []
    previous_color = detection_line[0]
    previous_border_index = 0

    for i, pixel in enumerate(detection_line):
        if not np.array_equal(previous_color, pixel):
            sections.append((previous_border_index, i - 1))
            previous_border_index = i
            previous_color = pixel

    return sections


def _filter_noise(sections: List[Section], minimum_key_width: int) -> List[Section]:
    return list(filter(lambda section: section.end - section.start > minimum_key_width, sections))


def _get_key_color(detection_line: np.ndarray, section: Section) -> KeyColor:
    color = Color.from_bgr(*detection_line[section.start])
    return KeyColor.BLACK_KEY if color.closer_to(BLACK, WHITE) == BLACK else KeyColor.WHITE_KEY
