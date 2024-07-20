from typing import Iterator

import cv2
from cv2 import VideoCapture

from globals.global_types import Image


class Video:
    def __init__(self, video_file_path: str):
        self.capture = VideoCapture(video_file_path)

    @property
    def fps(self):
        return self.capture.get(cv2.CAP_PROP_FPS)

    def extract_frames(self) -> Iterator[Image]:
        while self.capture.isOpened():
            _, frame = self.capture.read()
            yield frame
        self.capture.release()
