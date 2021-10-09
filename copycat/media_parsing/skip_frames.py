from typing import Iterator


def skip_frames(amount_of_frames_to_skip: int, frames: Iterator) -> None:
    for i in range(amount_of_frames_to_skip):
        next(frames)
