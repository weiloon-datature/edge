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
@Desc    :   TF Object Detection Predictor class.
"""

import numpy as np
import tensorflow as tf
from abstract_predictor import AbstractPredictor
from common.constants import MODEL_ARCH, OUTPUT_LAYERS
from common.exceptions import (
    InvalidModelInputException,
    InvalidModelOutputException,
    PredictionException,
)


class Predictor(AbstractPredictor):

    """TF Object Detection Predictor class."""

    def __init__(self, model, category_index, color_map, **kwargs):
        """Initialize TF Predictor.

        Args:
            model: TF SavedModel.
            category_index: Class labels map.
            color_map: Color map for bounding boxes.
        """
        super().__init__(model, category_index, color_map, **kwargs)
        self._preprocess_func = getattr(
            self, f"_{self.model_architecture}_preprocess"
        ) if self.model_architecture in MODEL_ARCH[
            self.model_format] else getattr(self, "_preprocess")
        self._postprocess_func = getattr(
            self, f"_{self.model_architecture}_postprocess"
        ) if self.model_architecture in MODEL_ARCH[
            self.model_format] else getattr(self, "_postprocess")
        self._detections_output = {}

    def predict(self, img):
        """Predict on image.

        Args:
            img: Image to predict on.

        Returns:
            Dictionary of predictions containing bounding boxes, classes and scores.

        Raises:
            PredictionException: If prediction fails.
        """
        try:
            # Feed image into model
            model_input = self._preprocess_func(img)
            self._detections_output = self._model(model_input)
            return self._postprocess_func()
        except Exception as exc:
            raise PredictionException(exc) from exc

    def _preprocess(self, img):
        """Preprocess image to be compatible with the model.

        Args:
            img: Image to preprocess.

        Returns:
            Input tensor batch.

        Raises:
            InvalidModelInputException: If input is not a tensor.
        """
        try:
            # The input needs to be a tensor,
            # convert it using `tf.convert_to_tensor`.
            input_tensor = tf.convert_to_tensor(img)

            # The model expects a batch of images,
            # so add an axis with `tf.newaxis`.
            input_tensor = input_tensor[tf.newaxis, ...]
        except Exception as exc:
            raise InvalidModelInputException(exc) from exc
        return input_tensor

    def _postprocess(self):
        """Postprocess raw model output into interpretable predictions.

        Returns:
            Dictionary of predictions containing bounding boxes, classes and scores.

        Raises:
            InvalidModelOutputException: If output cannot be parsed.
        """
        try:
            num_detections = int(self._detections_output.pop("num_detections"))
            if num_detections == 0:
                return {"boxes": [], "classes": [], "scores": []}

            detections = {
                key: value[0, :num_detections].numpy()
                for key, value in self._detections_output.items()
            }
            detections["num_detections"] = num_detections

            output_layer_names = OUTPUT_LAYERS[self.detection_type][
                self.model_format]

            # Filter out predictions below threshold
            indexes = np.where(detections[output_layer_names["scores"]] >
                               float(self.threshold))
            boxes = detections[output_layer_names["boxes"]][indexes]
            classes = detections[
                output_layer_names["classes"]][indexes].astype(np.int64)
            scores = detections[output_layer_names["scores"]][indexes]
        except Exception as exc:
            raise InvalidModelOutputException(exc) from exc

        predictions_output = {
            "boxes": boxes.tolist(),
            "classes": classes.tolist(),
            "scores": scores.tolist()
        }
        return predictions_output

    def _yolov4_preprocess(self, img):
        """Preprocess image to be compatible with the model.

        Args:
            img: Image to preprocess.

        Returns:
            Input tensor batch.

        Raises:
            InvalidModelInputException: If input is not a tensor.
        """
        # TODO: Implement YOLOv4 preprocessing for TF

    def _yolov4_postprocess(self):
        """Postprocess raw model output into interpretable predictions.

        Returns:
            Dictionary of predictions containing bounding boxes, classes and scores.

        Raises:
            InvalidModelOutputException: If output cannot be parsed.
        """
        # TODO: Implement YOLOv4 postprocessing for TF
