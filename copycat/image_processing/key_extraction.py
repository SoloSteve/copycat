from typing import List, Tuple, Optional

import numpy as np
from tqdm import tqdm

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
    sections = _filter_noise(sections, 5)

    piano_keys = []

    for i, section in tqdm(enumerate(sections), desc="Parsing keys"):
        piano_keys.append(
            PianoKey(
                absolute_index=i + key_offset,
                section=Section(section[0], section[1])
            )
        )
    return piano_keys


def automatically_detect_keyboard_line(control_frame: Image) -> Optional[int]:
    """
     The algorithm used to detect where the keyboard is:
     1. Go through each horizontal line on the frame
     2. Everytime there is a significant color change, we save its coordinates, we treat each color change as a key.
     3. Remove noise by filtering things that are two small to be keys
     4. We check to see if what we think are keys really are keys by making sure they're all relatively the same size.
     5. We check to see that the ratio black to white keys is 5 black keys per 7 white keys.
     6. We give a percentage of how accurate our previous 2 checks were.
     7. If we get 100 lines in a row where the accuracy percentage is over 80%, we treat that as the keyboard

    :return: The height of a location on the keyboard.
    """
    frame_height = control_frame.shape[0]
    binary_frame = reduce_colors(control_frame, 2)
    guess_counter = 0
    with tqdm(total=frame_height, desc="Attempting to automatically detect piano keyboard...") as pbar:
        for i in range(1, frame_height):
            pbar.update(1)
            section = _get_sections_by_border_detection(binary_frame[i])
            filtered_section = _filter_noise(section, 5)
            if len(filtered_section) < 12:
                continue
            guess = _get_keyboard_guess_percentage(filtered_section, binary_frame[i], 5)
            if guess > 0.8:
                guess_counter += 1
            else:
                guess_counter = 0

            if guess_counter == 100:
                pbar.update(frame_height - i)
                return i
    return None


def _get_sections_by_border_detection(detection_line: np.ndarray) -> List[Tuple[int, int]]:
    """
    Split an array of pixels each time there is a change in color.

    Take for example an array:

    |0|0|0|0|0|1|1|1|1|1|1|0|0|0|0|

    This would be split every time we change from 0 to 1 or from 1 to 0
    The result would be the two indexes at which that change occurs (on either side of the key, marking its borders).

    :return: The "x" and "x + width" coordinates of a key
    """
    sections = []
    previous_color = detection_line[0]
    previous_border_index = 0

    for i, pixel in enumerate(detection_line):
        if not np.array_equal(previous_color, pixel):
            sections.append((previous_border_index, i - 1))
            previous_border_index = i
            previous_color = pixel

    return sections


def _filter_noise(sections: List[Tuple[int, int]], minimum_key_width: int) -> List[Tuple[int, int]]:
    """
    Remove sections that are smaller than the minimum key width.
    """
    return list(filter(lambda section: section[1] - section[0] > minimum_key_width, sections))


def _get_key_color(detection_line: np.ndarray, section: Tuple[int, int]) -> KeyColor:
    """
    Checks whether the section is a black or white key.
    """
    color = Color.from_bgr(*detection_line[section[0]])
    return KeyColor.BLACK_KEY if color.closer_to(BLACK, WHITE) == BLACK else KeyColor.WHITE_KEY


def _get_keyboard_guess_percentage(
        sections: List[Tuple[int, int]],
        detection_line: np.ndarray,
        max_separation: int
) -> float:
    """
    Returns a percentage (0 to 1) of how confident we are that this is part of the piano keyboard.
    """
    white_widths = [end - start for start, end in sections if
                    _get_key_color(detection_line, (start, end)) == KeyColor.WHITE_KEY]
    black_widths = [end - start for start, end in sections if
                    _get_key_color(detection_line, (start, end)) == KeyColor.BLACK_KEY]
    if len(white_widths) == 0 or len(black_widths) == 0:
        return 0

    white_average_width = sum(white_widths) / len(white_widths)
    black_average_width = sum(black_widths) / len(black_widths)
    uniformity_counter = 0
    for width in white_widths:
        if white_average_width - max_separation < width < white_average_width + max_separation:
            uniformity_counter += 1

    for width in black_widths:
        if black_average_width - max_separation < width < black_average_width + max_separation:
            uniformity_counter += 1

    uniformity_percentage = uniformity_counter / len(sections)
    black_to_white_percentage = np.clip(1 - (abs((len(black_widths) / len(white_widths)) - 0.7)), 0, 1)
    return round((uniformity_percentage + black_to_white_percentage) / 2, 2)
