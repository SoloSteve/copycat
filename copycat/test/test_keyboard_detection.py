from cv2 import cv2
from copycat.image_processing.key_extraction import automatically_detect_keyboard_line


def test_video_one():
    value = automatically_detect_keyboard_line(cv2.imread("images/fullscreen_youtube_capture.png"))
    print(value)
    assert 800 < value < 950


def test_video_two():
    value = automatically_detect_keyboard_line(cv2.imread("images/fullscreen_youtube_capture2.png"))
    print(value)
    assert 760 < value < 880
