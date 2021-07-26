from typing import List, Iterable

import cv2

from copycat.global_types import Image
from processing.paino_key import PianoKey


def show_video(video: Iterable[Image]):
    for frame in video:
        cv2.imshow('frame', frame)
        if cv2.waitKey(20) != -1:
            return


def show_contours(original_image, contours: List, slideshow=0):
    print(f"number of contours: {len(contours)}")
    image = original_image
    for contour in contours:
        if slideshow:
            image = original_image.copy()
        image = __outline_contour(image, contour)
        if slideshow:
            cv2.imshow("contoured", image)
            cv2.waitKey(slideshow)
            cv2.destroyWindow("contoured")
    if not slideshow:
        cv2.imshow("contoured", image)


def show_contours_for_keys(original_image, keys: Iterable[PianoKey]):
    image = original_image.copy()
    for key in keys:
        print(key.note)
        show_contours(image, [key.contour])
        cv2.waitKey()


def draw_line(original_image, line_height):
    image = original_image.copy()
    cv2.line(image, (0, line_height), (image.shape[1], line_height), (36, 255, 12), 3)
    return image


def draw_circle(original_image, x, y):
    image = original_image.copy()
    cv2.circle(image, (x, y), 3, (36, 255, 12), 3)
    return image


def __outline_contour(base_image, contour):
    image = base_image.copy()
    x, y, w, h = cv2.boundingRect(contour)
    cv2.rectangle(image, (x, y), (x + w, y + h), (36, 255, 12), 3)
    return image
