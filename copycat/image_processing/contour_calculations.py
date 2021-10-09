from typing import Iterable

import numpy as np
from cv2 import cv2

from globals.global_types import Contour, Image, Bounds


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
