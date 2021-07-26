from typing import Iterator

from cv2 import VideoCapture

from copycat.global_types import Image


def extract_frames(video_file_path: str) -> Iterator[Image]:
    capture = VideoCapture(video_file_path)
    while capture.isOpened():
        _, frame = capture.read()
        yield frame
    capture.release()
