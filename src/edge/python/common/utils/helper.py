#!/usr/bin/python3.7
# -*-coding:utf-8 -*-
"""
  ████
██    ██   Datature
  ██  ██   Powering Breakthrough AI
    ██

@File    :   helper.py
@Author  :   Wei Loon Cheng
@Version :   1.0
@Contact :   hello@datature.io
@License :   Apache License 2.0
@Desc    :   General helper functions.
"""

import numpy as np


def load_image_into_numpy_array(img, input_shape):
    """Load an image from base64 into a numpy array.

    Puts image into numpy array to feed into tensorflow graph.
    Note that by convention we put it into a numpy array with shape
    (height, width, channels), where channels=3 for RGB.

    Args:
        image_base64: image in base64 format
        height: height of image
        width: width of image

    Returns:
        uint8 numpy array with shape (img_height, img_width, 3)
    """
    image_shape = np.asarray(img).shape
    image_resized = img.resize(input_shape)

    return np.array(image_resized), (image_shape[0], image_shape[1])
