from typing import Iterator

from globals.global_types import Image, Bounds


def crop_video(frames: Iterator[Image], bounds: Bounds) -> Iterator[Image]:
    for frame in frames:
        yield crop(frame, bounds)


def crop(image: Image, bounds: Bounds) -> Image:
    """
    Crops the image

    :param image: The image to crop
    :param bounds: The bounds that dictate where to crop
    :return: A cropped image
    """
    return image[bounds.y:(bounds.y + bounds.height), bounds.x:(bounds.x + bounds.width)]
