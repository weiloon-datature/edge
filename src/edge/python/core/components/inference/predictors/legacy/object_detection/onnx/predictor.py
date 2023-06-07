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
from common.constants import MODEL_ARCH, OUTPUT_LAYERS, YOLO_ANCHORS
from common.exceptions import (
    InvalidModelInputException,
    InvalidModelOutputException,
    PredictionException,
)
from common.utils import yolo_postprocess, yolov3v4_postprocess


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

        if self.model_architecture in ["yolox"]:
            _, _, height, width = self._model.get_inputs()[0].shape
        else:
            _, height, width, _ = self._model.get_inputs()[0].shape
        if isinstance(height, int) and isinstance(width, int):
            self.input_shape = (height, width)
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
            model_input = self._preprocess_func(img)
            self._detections_output = self._model.run(
                self._output_names, {self._input_name: model_input})
            return self._postprocess_func()
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
            input_image = np.expand_dims(img.astype(np.uint8), axis=0)
        except Exception as exc:
            raise InvalidModelInputException(exc) from exc
        return input_image

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
                self.model_format][self.model_architecture if self.
                                   model_architecture in
                                   MODEL_ARCH["onnx"] else "general"]
            for index, each_name in enumerate(self._output_names):
                if each_name in output_layer_names["boxes"]:
                    boxes = np.squeeze(self._detections_output[index])
                if each_name in output_layer_names["classes"]:
                    classes = np.squeeze(self._detections_output[index])
                if each_name in output_layer_names["scores"]:
                    scores = np.squeeze(self._detections_output[index])
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

    def _yolov4_preprocess(self, img):
        """Preprocess image to be compatible with the YOLOV4 model.

        Args:
            img: Image to preprocess.

        Returns:
            Preprocessed image.

        Raises:
            InvalidModelInputException: If input is not a numpy array.
        """
        try:
            input_image = np.expand_dims((img / 255).astype(np.float32),
                                         axis=0)
        except Exception as exc:
            raise InvalidModelInputException(exc) from exc
        return input_image

    def _yolov4_postprocess(self):
        """Postprocess YOLOV4 raw model output into interpretable predictions.

        Returns:
            Dictionary of predictions containing bounding boxes, classes and scores.

        Raises:
            InvalidModelOutputException: If output cannot be parsed.
        """
        try:
            boxes, classes, scores = yolov3v4_postprocess(
                self._detections_output,
                self.input_shape,
                YOLO_ANCHORS,
                len(self.category_index),
                self.input_shape,
            )
            if boxes == []:
                return {"boxes": [], "classes": [], "scores": []}

            indexes = np.where(scores > float(self.threshold))  # type: ignore

            boxes = boxes[indexes]
            classes = classes[indexes]
            scores = scores[indexes]
        except Exception as exc:
            raise InvalidModelOutputException(exc) from exc

        predictions_output = {
            "boxes": boxes.tolist(),
            "classes": classes.tolist(),
            "scores": scores.tolist()
        }
        return predictions_output

    def _yolox_preprocess(self, img):
        """Preprocess image to be compatible with the YOLOX model.

        Args:
            img: Image to preprocess.

        Returns:
            Preprocessed image.

        Raises:
            InvalidModelInputException: If input is not a numpy array.
        """
        try:
            input_image = np.expand_dims(
                img.astype(np.float32).transpose(2, 0, 1), 0)
        except Exception as exc:
            raise InvalidModelInputException(exc) from exc
        return input_image

    def _yolox_postprocess(self):
        """Postprocess YOLOX raw model output into interpretable predictions.

        Returns:
            Dictionary of predictions containing bounding boxes, classes and scores.

        Raises:
            InvalidModelOutputException: If output cannot be parsed.
        """
        try:
            output = yolo_postprocess(self._detections_output[0],
                                      num_classes=3,
                                      conf_thre=self.threshold)[0]
            if output is None:
                return {"boxes": [], "classes": [], "scores": []}

            boxes = output[:, 0:4].cpu().detach().numpy().astype(np.float64)
            classes = output[:, 6].cpu().detach().numpy().astype(np.float64)
            scores = (output[:, 4] *
                      output[:, 5]).cpu().detach().numpy().astype(np.float64)
            boxes = [[
                bbox[1] / self.input_shape[0],
                bbox[0] / self.input_shape[1],
                bbox[3] / self.input_shape[0],
                bbox[2] / self.input_shape[1],
            ] for bbox in boxes]
        except Exception as exc:
            raise InvalidModelOutputException(exc) from exc

        predictions_output = {
            "boxes": boxes,
            "classes": classes,
            "scores": scores
        }
        return predictions_output
