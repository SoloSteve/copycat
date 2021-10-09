from typing import Dict

from copycat.media_parsing.crop import crop
from globals.global_types import Image, Bounds
from globals.paino_key import KeyColor, PianoKeyContour
from image_processing.contour_calculations import _format_contours, _sort_contours, _get_contours_for_white_keys, \
    _get_contours_for_black_keys
from image_processing.image_manipulations import reduce_colors


def get_piano_keys_by_contour(control_frame: Image, bounds: Bounds, white_key_offset: int) -> Dict[str, PianoKeyContour]:
    """
    !!! Deprecated !!!

    Extracts the keys using contour detection
    """
    keys = {}
    control_frame = crop(control_frame, bounds)
    binary_keyboard_color = reduce_colors(control_frame, 2)
    white_key_contours = _format_contours(_sort_contours(_get_contours_for_white_keys(binary_keyboard_color)), bounds)
    black_key_contours = _format_contours(_sort_contours(_get_contours_for_black_keys(binary_keyboard_color)), bounds)

    for index_in_contour, contour in enumerate(white_key_contours):
        piano_key = PianoKeyContour(
            contour=contour,
            key_color=KeyColor.WHITE_KEY,
            white_key_offset=white_key_offset,
            local_index=index_in_contour
        )
        keys[piano_key.note] = piano_key

    for index_in_contour, contour in enumerate(black_key_contours):
        piano_key = PianoKeyContour(
            contour=contour,
            key_color=KeyColor.BLACK_KEY,
            white_key_offset=white_key_offset,
            local_index=index_in_contour
        )
        keys[piano_key.note] = piano_key

    return keys
