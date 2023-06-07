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
from common.constants import OUTPUT_LAYERS
from common.exceptions import (
    InvalidModelInputException,
    InvalidModelOutputException,
    PredictionException,
)


class Predictor(AbstractPredictor):

    """TFLite Object Detection Predictor class."""

    def __init__(self, model, category_index, color_map, **kwargs):
        """Initialize TFLite Predictor.

        Args:
            model: TFLite interpreter.
            category_index: Class labels map.
            color_map: Color map for bounding boxes.
        """
        super().__init__(model, category_index, color_map, **kwargs)
        self._input_details = self._model.get_input_details()
        self._output_details = self._model.get_output_details()
        _, height, width, _ = self._model.get_input_details()[0]['shape']
        if isinstance(height, int) and isinstance(width, int):
            self.input_shape = (height, width)

    def predict(self, img):
        """Predict on image.

        Args:
            img: Image to predict on.

        Returns:
            Dictionary of predictions containing bounding boxes, classes and scores.

        Raises:
            PredictionException: If prediction fails.
        """
        # Run prediction
        try:
            model_input = self._preprocess(img)
            self._model.set_tensor(self._input_details[0]['index'],
                                   model_input)
        except Exception as exc:
            raise InvalidModelInputException(exc) from exc
        try:
            self._model.invoke()
        except Exception as exc:
            raise PredictionException(exc) from exc
        return self._postprocess()

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
            return [img.astype(np.float32)]
        except Exception as exc:
            raise InvalidModelInputException(exc) from exc

    def _postprocess(self):
        """Postprocess raw model output into interpretable predictions.

        Returns:
            Dictionary of predictions containing bounding boxes, classes and scores.

        Raises:
            InvalidModelOutputException: If output cannot be parsed.
        """
        boxes = []
        classes = []
        scores = []

        # Extract data and filter against desired threshold
        try:
            output_layer_names = OUTPUT_LAYERS[self.detection_type][
                self.model_format]
            for each_layer in self._output_details:
                if each_layer["name"] in output_layer_names["boxes"]:
                    boxes = np.squeeze(
                        self._model.get_tensor(each_layer['index']))
                if each_layer["name"] in output_layer_names["classes"]:
                    classes = np.squeeze(
                        self._model.get_tensor(each_layer['index']))
                if each_layer["name"] in output_layer_names["scores"]:
                    scores = np.squeeze(
                        self._model.get_tensor(each_layer['index']))
            if len(scores) == 0:
                return {"boxes": [], "classes": [], "scores": []}

            # Filter out predictions below threshold
            indexes = np.where(scores > float(self.threshold))  # type: ignore

            # Extract predictions
            scores = scores[indexes]
            boxes = boxes[indexes]
            classes = classes[indexes]
        except Exception as exc:
            raise InvalidModelOutputException(exc) from exc

        predictions_output = {
            "boxes": boxes.tolist(),
            "classes": classes.tolist(),
            "scores": scores.tolist()
        }
        return predictions_output
