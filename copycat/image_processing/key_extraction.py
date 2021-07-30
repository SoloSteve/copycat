from typing import Dict, Iterable

import cv2
import numpy as np

from global_types import Image, Contour, Bounds
from media_parsing.crop import crop
from image_processing.paino_key import ColorFamily, PianoKey


def get_piano_keys(control_frame: Image, bounds: Bounds, white_key_offset: int) -> Dict[str, PianoKey]:
    keys = {}
    control_frame = crop(control_frame, bounds)
    binary_keyboard_color = _reduce_colors(control_frame, 2)
    white_key_contours = _format_contours(_sort_contours(_get_contours_for_white_keys(binary_keyboard_color)), bounds)
    black_key_contours = _format_contours(_sort_contours(_get_contours_for_black_keys(binary_keyboard_color)), bounds)

    for index_in_contour, contour in enumerate(white_key_contours):
        piano_key = PianoKey(
            contour=contour,
            color_family=ColorFamily.WHITE_KEY,
            white_key_offset=white_key_offset,
            local_index=index_in_contour
        )
        keys[piano_key.note] = piano_key

    for index_in_contour, contour in enumerate(black_key_contours):
        piano_key = PianoKey(
            contour=contour,
            color_family=ColorFamily.BLACK_KEY,
            white_key_offset=white_key_offset,
            local_index=index_in_contour
        )
        keys[piano_key.note] = piano_key

    return keys


def _reduce_colors(image: Image, number_of_colors: int) -> Image:
    """
    Reduce image colors using "kmeans cluster" algorithm

    https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_ml/py_kmeans/py_kmeans_opencv/py_kmeans_opencv.html#color-quantization

    :param image: The image whose colors will be reduced.
    :param number_of_colors: The number of different colors that will be used to make up the new image.
    :return: The new image with reduced colors
    """
    reshaped = image.reshape((-1, 3))

    # convert to np.float32
    reshaped = np.float32(reshaped)

    # define criteria, number of clusters(K) and apply kmeans()
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 10.0)
    ret, label, center = cv2.kmeans(reshaped, number_of_colors, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

    # Now convert back into uint8, and make original image
    center = np.uint8(center)
    res = center[label.flatten()]
    return res.reshape(image.shape)  # , center


def _sort_contours(contours: Iterable[Contour], method="left-to-right"):
    # initialize the reverse flag and sort index
    reverse = False
    i = 0
    # handle if we need to sort in reverse
    if method == "right-to-left" or method == "bottom-to-top":
        reverse = True
    # handle if we are sorting against the y-coordinate rather than
    # the x-coordinate of the bounding box
    if method == "top-to-bottom" or method == "bottom-to-top":
        i = 1
    # construct the list of bounding boxes and sort them from top to
    # bottom
    bounding_boxes = [cv2.boundingRect(c) for c in contours]
    (contours, bounding_boxes) = zip(*sorted(zip(contours, bounding_boxes),
                                             key=lambda b: b[1][i], reverse=reverse))
    # return the list of sorted contours and bounding boxes
    return contours  # , bounding_boxes


def _get_contours_for_black_keys(control_img: Image):
    gray = cv2.cvtColor(control_img, cv2.COLOR_BGR2GRAY)
    kernel = np.ones((10, 10), np.uint8)
    dilated = cv2.dilate(gray, kernel)
    _, thresh1 = cv2.threshold(dilated, 127, 255, cv2.THRESH_BINARY_INV)
    cnts, _ = cv2.findContours(thresh1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return cnts


def _get_contours_for_white_keys(control_img: Image):
    gray = cv2.cvtColor(control_img, cv2.COLOR_BGR2GRAY)
    _, thresh1 = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    cnts, _ = cv2.findContours(thresh1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return list(filter(__is_contour_noise, cnts))


def __is_contour_noise(contour: Contour, threshold_area=100):
    area = cv2.contourArea(contour)
    return area > threshold_area


def _format_contours(contours, bounds: Bounds):
    for contour in contours:
        for point in contour:
            point[0][0] += bounds.x
            point[0][1] += bounds.y

    return contours
