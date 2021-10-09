from typing import List, Iterable

import cv2

from globals.global_types import Image, Bounds
from globals.paino_key import PianoKey, PianoKeyContour


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


def draw_contours_for_keys(original_image, keys: Iterable[PianoKeyContour]):
    image = original_image.copy()
    for key in keys:
        bounds = Bounds(*cv2.boundingRect(key.__contour))
        cv2.putText(image, key.note, (bounds.x + round(bounds.width / 10), bounds.y + round(bounds.height / 2)),
                    cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.4, color=(255, 105, 180))
        __outline_contour(image, key.__contour)
    return image


def draw_notes_for_keys(original_image, keys: Iterable[PianoKey], detection_height):
    image = original_image.copy()
    for key in keys:
        cv2.putText(image, key.note,
                    (key.section.start + round((key.section.end - key.section.start) / 10), detection_height - 50),
                    cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.4, color=(255, 105, 180))
    return image


def draw_detector_line(original_image, line_height):
    cv2.imshow("detector_line", draw_line(original_image, line_height))
    cv2.waitKey()
    cv2.destroyWindow("detector_line")


def draw_circle(original_image, x, y):
    image = original_image.copy()
    cv2.circle(image, (x, y), 3, (36, 255, 12), 3)
    return image


def draw_rectangle(original_image, x, y, w, h):
    image = original_image.copy()
    cv2.rectangle(image, (x, y), (x + w, y + h), (36, 255, 12), 3)
    return image


def draw_line(original_image, line_height):
    image = original_image.copy()
    cv2.line(image, (0, line_height), (image.shape[1], line_height), (0, 191, 255), 3)
    return image


def __outline_contour(base_image, contour):
    image = base_image.copy()
    x, y, w, h = cv2.boundingRect(contour)
    cv2.rectangle(image, (x, y), (x + w, y + h), (36, 255, 12), 3)
    return image


def debug_params(control_frame, keys, detector, bounds=None):
    image = control_frame.copy()
    if bounds is not None:
        image = draw_rectangle(image, bounds.x, bounds.y, bounds.width, bounds.height)
    image = draw_line(image, detector._detection_height)
    if isinstance(keys[0], PianoKeyContour):
        image = draw_contours_for_keys(image, keys.values())
    else:
        image = draw_notes_for_keys(image, keys, detector._detection_height)
    cv2.imshow("debug", image)
    cv2.waitKey()
