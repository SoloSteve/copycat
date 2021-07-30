import cv2
import numpy as np

from global_types import Image, Contour
from image_processing.color import Color


class NoteDetector:
    def __init__(self, control_frame: Image, detection_height: int, detection_threshold: float):
        self._detection_height = detection_height
        self._detection_threshold = detection_threshold
        self._control_detection_line = control_frame[detection_height]

    def is_note_detected(self, contour: Contour, image: Image) -> bool:
        contour_x, _, contour_width, _ = cv2.boundingRect(contour)
        control_color = _get_mean_color_at_slice(self._control_detection_line[contour_x: contour_x + contour_width])

        checked_color = _get_mean_color_at_slice(image[self._detection_height][contour_x: contour_x + contour_width])
        return control_color.diff(checked_color) >= self._detection_threshold


def _get_mean_color_at_slice(color_slice: np.ndarray) -> Color:
    return Color.from_bgr(*color_slice.mean(axis=0))
