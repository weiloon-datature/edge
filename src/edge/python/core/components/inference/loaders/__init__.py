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
@Desc    :   Package for model loaders.
"""

from importlib import import_module

from common.config import CONFIG
from common.exceptions import UnsupportedModelFormatException

try:
    model_format = CONFIG["inference"]["model_format"]
    if "legacy" in CONFIG["inference"]:
        loader_module = f"loaders.legacy.{model_format}.loader"
    else:
        loader_module = f"loaders.{model_format}.loader"
    Loader = import_module(loader_module).Loader
except Exception as exc:
    raise UnsupportedModelFormatException(
        f"Model format {CONFIG['inference']['model_format']} not supported!"
    ) from exc

__all__ = ["Loader"]
