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
@Desc    :   ONNX Object Detection Predictor class.
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

    """ONNX Object Detection Predictor class."""

    def __init__(self, model, category_index, color_map, **kwargs):
        """Initialize ONNX Predictor.

        Args:
            model: ONNX InferenceSession.
            category_index: Class labels map.
            color_map: Color map for bounding boxes.
        """
        super().__init__(model, category_index, color_map, **kwargs)
        self._input_name = self._model.get_inputs()[0].name
        self._output_names = [
            single_output.name for single_output in self._model.get_outputs()
        ]

        _, height, width, _ = self._model.get_inputs()[0].shape
        if isinstance(height, int) and isinstance(width, int):
            self.input_shape = (height, width)
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
            self._detections_output = self._model.run(
                self._output_names, {self._input_name: model_input})
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
            self._detections_output = self._detections_output[0][0]
            slicer = self._detections_output[:, -1]
            output = self._detections_output[:, :6][slicer != 0]
            scores = output[:, 4]
            output = output[scores > self.threshold]
            classes = output[:, 5]
            output = output[classes != 0]

            ## Postprocess detections
            boxes = output[:, :4]
            classes = output[:, 5].astype(np.int32)
            scores = output[:, 4]
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
