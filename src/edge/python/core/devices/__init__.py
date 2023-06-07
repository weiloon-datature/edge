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
@Desc    :   Package for device engine.
"""

from importlib import import_module

from common.config import CONFIG

from .abstract_engine import AbstractEngine

DeviceEngine = import_module(f"core.devices.{CONFIG['device']}.engine").Engine

__all__ = ["AbstractEngine", "DeviceEngine"]
