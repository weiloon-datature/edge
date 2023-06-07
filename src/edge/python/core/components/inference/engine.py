#!/usr/bin/python3.7
# -*-coding:utf-8 -*-
"""
  ████
██    ██   Datature
  ██  ██   Powering Breakthrough AI
    ██

@File    :   engine.py
@Author  :   Wei Loon Cheng
@Version :   1.0
@Contact :   hello@datature.io
@License :   Apache License 2.0
@Desc    :   Inference engine class.
"""

from common.config import CONFIG
from common.exceptions import (
    LoaderException,
    PredictionException,
    PredictorException,
    UnknownException,
)
from common.logger import Logger

from .loaders import Loader
from .predictors import Predictor


class InferenceEngine:

    """Inference engine class."""

    def __init__(self):
        """Initialize inference engine.

        Creates the loader which loads the model into memory
            and creates the predictor.

        Raises:
            LoaderException: If the loader fails to load the model.
            PredictorException: If the predictor fails to initialize.
        """
        try:
            self._loader = Loader(**CONFIG["inference"]).load_model()
        except LoaderException as exc:
            raise LoaderException(exc) from exc

        try:
            self._predictor = Predictor(self.loader.model,
                                        self.loader.category_index,
                                        self.loader.color_map,
                                        **CONFIG["inference"])
        except PredictorException as exc:
            raise PredictorException(exc) from exc

    def run(self, assets):
        """Run inference engine and calls the predictor to predict the frame.

        Args:
            assets (dict): Dictionary of assets.

        Raises:
            PredictionException: If the prediction fails.
            UnknownException: If an unknown exception occurs.
        """
        try:
            Logger.debug(f"Predicting frame {assets['frame_id']}!")
            assets["predictions"] = self.predictor.predict(
                assets["input_frame"])
        except PredictionException as exc:
            raise PredictionException(exc) from exc
        except UnknownException as exc:
            raise UnknownException(exc) from exc

    @property
    def loader(self):
        """Get loader.

        Returns:
            Loader: Loader module.
        """
        return self._loader

    @property
    def predictor(self):
        """Get predictor.

        Returns:
            Predictor: Predictor module.
        """
        return self._predictor

    @loader.setter
    def loader(self, loader):
        """Set loader.

        Args:
            loader (Loader): Loader module.
        """
        self._loader = loader

    @predictor.setter
    def predictor(self, predictor):
        """Set predictor.

        Args:
            predictor (Predictor): Predictor module.
        """
        self._predictor = predictor
