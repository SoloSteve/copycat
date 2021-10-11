from typing import Iterator

import cv2
from cv2 import VideoCapture

from globals.global_types import Image


class Video:
    def __init__(self, video_file_path: str):
        self.capture = VideoCapture(video_file_path)
        self.__fps = self.capture.get(cv2.CAP_PROP_FPS)
        self.__total_frames = self.capture.get(cv2.CAP_PROP_FRAME_COUNT)

    @property
    def fps(self):
        return self.__fps

    @property
    def total_frames(self):
        return self.__total_frames

    def extract_frames(self, seconds=-1) -> Iterator[Image]:
        if seconds != -1:
            self.__total_frames = seconds * self.fps
        elapsed_frames = 0
        while self.capture.isOpened():
            _, frame = self.capture.read()
            if frame is None:
                break
            yield frame
            elapsed_frames += 1
            if elapsed_frames >= seconds * self.fps and seconds != -1:
                break
        self.capture.release()
