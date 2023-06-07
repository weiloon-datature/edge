#!/usr/bin/python3.7
# -*-coding:utf-8 -*-
"""
  ████
██    ██   Datature
  ██  ██   Powering Breakthrough AI
    ██

@File    :   config.py
@Author  :   Wei Loon Cheng
@Version :   1.0
@Contact :   hello@datature.io
@License :   Apache License 2.0
@Desc    :   Configuration module.
"""

import os

from common.exceptions import InvalidConfigException, InvalidConfigPathException
from yaml import YAMLError
from yaml import load as yaml_load

try:
    from yaml import CLoader as YAMLLoader
except ImportError:
    from yaml import Loader as YAMLLoader

ROOT_DIR = str(os.environ.get("DATATURE_EDGE_ROOT_DIR"))

try:
    with open(str(os.environ.get("DATATURE_EDGE_PYTHON_CONFIG")),
              "r",
              encoding="utf-8") as config_file:
        try:
            CONFIG = yaml_load(config_file, Loader=YAMLLoader)
        except YAMLError as exc:
            raise InvalidConfigException(exc) from exc
except Exception as exc:
    raise InvalidConfigPathException(exc) from exc
