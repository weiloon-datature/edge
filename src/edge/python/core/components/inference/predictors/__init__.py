#!/usr/bin/python3.7
# -*-coding:utf-8 -*-
"""
  ████
██    ██   Datature
  ██  ██   Powering Breakthrough AI
    ██

@File    :   __init__.py
@Author  :   Wei Loon Cheng
@Version :   1.0
@Contact :   hello@datature.io
@License :   Apache License 2.0
@Desc    :   Package for model predictors.
"""

import importlib

from common.config import CONFIG
from common.exceptions import UnsupportedModelFormatException

try:
    detection_type = CONFIG["inference"]["detection_type"]
    segmentation_type = (f".{CONFIG['inference']['segmentation_type']}"
                         ) if detection_type == "segmentation" else ""
    model_format = CONFIG["inference"]["model_format"]
    if "legacy" in CONFIG["inference"]:
        predictor_module = (
            f"predictors.legacy.{detection_type}{segmentation_type}"
            f".{model_format}.predictor")
    else:
        predictor_module = (f"predictors.{detection_type}{segmentation_type}"
                            f".{model_format}.predictor")
    Predictor = importlib.import_module(predictor_module).Predictor
except Exception as exc:
    raise UnsupportedModelFormatException(
        f"Model format {CONFIG['inference']['model_format']} not supported!"
    ) from exc

__all__ = ["Predictor"]
