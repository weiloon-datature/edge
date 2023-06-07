#!/usr/bin/python3.7
# -*-coding:utf-8 -*-
"""
  ████
██    ██   Datature
  ██  ██   Powering Breakthrough AI
    ██

@File    :   predictor.py
@Author  :   Wei Loon Cheng
@Version :   1.0
@Contact :   hello@datature.io
@License :   Apache License 2.0
@Desc    :   TFLite Object Detection Predictor class.
"""

import numpy as np
from abstract_predictor import AbstractPredictor
from common.exceptions import (
    InvalidModelInputException,
    InvalidModelOutputException,
    PredictionException,
)
from common.utils import nms_boxes


class Predictor(AbstractPredictor):

    """PyTorch Object Detection Predictor class."""

    def __init__(self, model, category_index, color_map, **kwargs):
        """Initialize TFLite Predictor.

        Args:
            model: TFLite SavedModel.
            category_index: Class labels map.
            color_map: Color map for bounding boxes.
        """
        super().__init__(model, category_index, color_map, **kwargs)
        # TODO: Get input shape from model
        # self.input_shape =
        self._detections_output = {}

    def predict(self, img):
        """Predict on image.

        Args:
            img: Image to predict on.

        Returns:
            List of tuples containing bounding boxes, classes and scores.

        Raises:
            PredictionException: If prediction fails.
        """
        try:
            model_input = self._preprocess(img)
            self._detections_output = self._model(inputs=model_input)
            return self._postprocess()
        except Exception as exc:
            raise PredictionException(exc) from exc

    def _preprocess(self, img):
        """Preprocess image to be compatible with the model.

        Args:
            img: Image to preprocess.

        Returns:
            Preprocessed image.

        Raises:
            InvalidModelInputException: If input is not a numpy array.
        """
        try:
            input_image = np.expand_dims(img.astype(np.float32), axis=0)
        except Exception as exc:
            raise InvalidModelInputException(exc) from exc
        return input_image

    def _postprocess(self):
        """Postprocess raw model output into interpretable predictions.

        Returns:
            List of tuples containing bounding boxes, classes and scores.

        Raises:
            InvalidModelOutputException: If output cannot be parsed.
        """
        try:
            ## Filter detections
            _, scores, classes, boxes = list(self._detections_output.values())  # pylint: disable=W0632
            classes = classes.astype(np.int16)
            _filter = scores > self.threshold
            classes = classes[_filter]
            boxes = boxes[_filter]
            scores = scores[_filter]

            # Filter background class
            _filter = classes != 0
            classes = classes[_filter]
            boxes = boxes[_filter]
            scores = scores[_filter]

            ## Postprocess detections
            boxes[:, 0], boxes[:, 1] = (boxes[:, 1] * self.input_shape[1],
                                        boxes[:, 0] * self.input_shape[0])
            boxes[:, 2], boxes[:, 3] = (boxes[:, 3] * self.input_shape[1],
                                        boxes[:, 2] * self.input_shape[0])
            boxes, classes, scores = nms_boxes(boxes, classes, scores, 0.1)
            boxes = [[
                box[1] / self.input_shape[1],
                box[0] / self.input_shape[0],
                box[3] / self.input_shape[1],
                box[2] / self.input_shape[0],
            ] for box in boxes]  # y1, x1, y2, x2
        except Exception as exc:
            raise InvalidModelOutputException(exc) from exc

        predictions_output = {
            "boxes": boxes,
            "classes": classes,
            "scores": scores,
        }
        return predictions_output
