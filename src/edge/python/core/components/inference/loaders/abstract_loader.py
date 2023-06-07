#!/usr/bin/python3.7
# -*-coding:utf-8 -*-
"""
  ████
██    ██   Datature
  ██  ██   Powering Breakthrough AI
    ██

@File    :   abstract_loader.py
@Author  :   Wei Loon Cheng
@Version :   1.0
@Contact :   hello@datature.io
@License :   Apache License 2.0
@Desc    :   Abstract class for model loaders.
"""

import os
from abc import ABC, abstractmethod

import numpy as np
from common.constants import ModelFormat
from common.exceptions import (
    InvalidColorMapException,
    InvalidLabelMapException,
    InvalidModelConfigException,
    InvalidModelException,
    InvalidModelPathException,
    UnsupportedModelFormatException,
)
from common.logger import Logger

try:
    from packages.hub.src.datature_hub.hub import HubModel
except ModuleNotFoundError:
    from datature_hub.hub import HubModel


class AbstractLoader(ABC):

    """Abstract class for model loaders."""

    def __init__(self, **kwargs):
        """Initialize loader."""
        self.model_format = ""
        self.model_architecture = ""
        self.model_path = ""
        self.label_path = ""
        self.project_secret = ""
        self.model_key = ""
        self.hub_dir = None
        self._model = None
        self._category_index = {}
        self._color_map = {}
        self.__dict__.update(kwargs)

    def load_model(self):
        """Load model.

        Raises:
            `UnsupportedModelFormatException`: Model format is not supported.
            `InvalidModelConfigException`: Invalid model configuration.

        Returns: self
        """
        if not ModelFormat.has_value(self.model_format):
            raise UnsupportedModelFormatException(
                f"{self.model_format} is not a valid model format!")
        if self.model_path != "" and self.label_path != "":
            self._load_local_model()
        elif self.project_secret != "" and self.model_key != "":
            self._load_hub_model()
        else:
            raise InvalidModelConfigException(
                "Invalid arguments for model loading!")
        return self

    def _load_local_model(self):
        """Load model locally.

        Raises:
            InvalidModelPathException: Model path is not found.
            InvalidModelException: Error loading model.
            InvalidLabelMapException: Error loading label map.
            InvalidColorMapException: Error loading color map.
        """
        if not os.path.exists(self.model_path):
            raise InvalidModelPathException(f"{self.model_path} is not found!")

        Logger.info(f"Loading {self.model_format} model...")
        try:
            self._load()
        except Exception as exc:
            raise InvalidModelException(
                f"Error loading {self.model_format} model!") from exc
        Logger.info(f"{self.model_format} model loaded!")

        try:
            self._load_label_map()
        except Exception as exc:
            raise InvalidLabelMapException("Error loading label map!") from exc

        try:
            self._load_color_map()
        except Exception as exc:
            raise InvalidColorMapException("Error loading color map!") from exc

    @abstractmethod
    def _load(self):
        """Load format-specific model.

        Raises:
            NotImplementedError: Abstract method.
        """
        raise NotImplementedError

    def _load_hub_model(self):
        """Load model using Datature Hub.

        Raises:
            InvalidModelException: Error loading model.
            InvalidLabelMapException: Error loading label map.
            InvalidColorMapException: Error loading color map.
        """
        Logger.info(f"Loading {self.model_format} model...")
        try:
            hub = HubModel(model_key=self.model_key,
                           project_secret=self.project_secret,
                           hub_dir=self.hub_dir)
            self._model = hub.load_model(self.model_format)
        except Exception as exc:
            raise InvalidModelException(
                f"Error loading {self.model_format} model!") from exc
        Logger.info(f"{self.model_format} model loaded!")

        try:
            self._category_index = hub.load_label_map()
        except Exception as exc:
            raise InvalidLabelMapException("Error loading label map!") from exc

        try:
            self._load_color_map()
        except Exception as exc:
            raise InvalidColorMapException("Error loading color map!") from exc

    def _load_label_map(self):
        """Read label map in the format of .txt and parse into dictionary.

        Raises:
            FileNotFoundError: If file path to the label map is invalid.
            ValueError: If label map is empty.
        """
        Logger.debug("Loading label map...")
        if not os.path.exists(self.label_path):
            raise FileNotFoundError("No valid label map found.")

        with open(self.label_path, "r", encoding="utf-8") as label_file:
            # If labels file is in JSON format
            lines = label_file.readlines()
            if "item" in lines[0]:
                for i, line in enumerate(lines):
                    if "id:" in line:
                        label_index = int(line.split(":")[-1])
                        label_name = lines[i +
                                           1].split(":")[-1].strip().strip('"')
                        self._category_index[label_index] = {
                            "id": label_index,
                            "name": label_name
                        }
            # If labels file is a list of class names
            else:
                idx = 1
                for line in lines:
                    self._category_index[idx] = {"id": idx, "name": line}
                    idx += 1
        self._category_index[0] = {"id": 0, "name": "background"}

        if not self._category_index:
            raise ValueError("Label map is empty!")
        Logger.debug("Label map loaded!")

    def _load_color_map(self):
        """Load color map.

        Raises:
            ValueError: If color map is empty.
        """
        Logger.debug("Loading color map...")
        for each_class in range(len(self._category_index)):
            self._color_map[each_class] = [
                int(i) for i in np.random.choice(range(256), size=3)
            ]

        if not self._color_map:
            raise ValueError("Color map is empty!")
        Logger.debug("Color map loaded!")

    @property
    def model(self):
        """Get loaded model."""
        return self._model

    @model.setter
    def model(self, model):
        """Set loaded model."""
        self._model = model

    @property
    def category_index(self):
        """Get category index."""
        return self._category_index

    @category_index.setter
    def category_index(self, category_index):
        """Set category index."""
        self._category_index = category_index

    @property
    def color_map(self):
        """Get color map."""
        return self._color_map

    @color_map.setter
    def color_map(self, color_map):
        """Set color map."""
        self._color_map = color_map
