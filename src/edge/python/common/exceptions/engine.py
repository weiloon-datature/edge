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
@Desc    :   Engine exceptions.
"""


class EngineException(Exception):

    """Base class for exceptions in the engine."""


class InputModuleException(EngineException):

    """Input module exception."""


class OutputModuleException(EngineException):

    """Output module exception."""


class InferenceModuleException(EngineException):

    """Model module exception."""


class PreprocessingModuleException(EngineException):

    """Preprocessing module exception."""


class PostprocessingModuleException(EngineException):

    """Postprocessing module exception."""


class CPUEngineException(EngineException):

    """CPU engine exception."""


class RaspberryPiEngineException(EngineException):

    """Raspberry Pi engine exception."""


class JetsonNanoEngineException(EngineException):

    """Jetson Nano engine exception."""
