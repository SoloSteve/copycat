import cv2
import numpy as np

from globals.global_types import Image


def reduce_colors(image: Image, number_of_colors: int) -> Image:
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
