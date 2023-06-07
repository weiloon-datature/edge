#!/usr/bin/python3.7
# -*-coding:utf-8 -*-
"""
  ████
██    ██   Datature
  ██  ██   Powering Breakthrough AI
    ██

@File    :   inference.py
@Author  :   Wei Loon Cheng
@Version :   1.0
@Contact :   hello@datature.io
@License :   Apache License 2.0
@Desc    :   Inference constants.
"""

from enum import Enum

import numpy as np


class ModelFormat(Enum):

    """Model format enum."""

    TF = "tf"
    TFLITE = "tflite"
    ONNX = "onnx"
    PYTORCH = "pytorch"

    @classmethod
    def has_value(cls, value):
        """Check if enum contains value.

        Args:
            value: Value to check.

        Returns:
            True if value is in enum, False otherwise.
        """
        return value in cls._value2member_map_


MODEL_ARCH = {
    "onnx": ["yolov4", "yolox"],
    "tf": ["yolov4"],
}

OUTPUT_LAYERS = {
    "object_detection": {
        "tf": {
            "boxes": "detection_boxes",
            "classes": "detection_classes",
            "scores": "detection_scores",
        },
        "tflite": {
            "boxes": ["detection_boxes", "StatefulPartitionedCall:3"],
            "classes": ["detection_classes", "StatefulPartitionedCall:2"],
            "scores": ["detection_scores", "StatefulPartitionedCall:1"],
        },
        "onnx": {
            "general": {
                "boxes": ["detection_boxes", "StatefulPartitionedCall:3"],
                "classes": ["detection_classes", "StatefulPartitionedCall:2"],
                "scores": ["detection_scores", "StatefulPartitionedCall:1"],
            },
        },
    },
    "segmentation": {},
}

YOLO_ANCHORS = np.array([
    [12., 16.],
    [19., 36.],
    [40., 28.],
    [36., 75.],
    [76., 55.],
    [72., 146.],
    [142., 110.],
    [192., 243.],
    [459., 401.],
])

TEST = 1
