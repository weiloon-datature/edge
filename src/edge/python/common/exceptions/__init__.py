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
@Desc    :   Package for common exceptions.
"""

from .config import InvalidConfigException, InvalidConfigPathException
from .engine import (
    CPUEngineException,
    EngineException,
    InferenceModuleException,
    InputModuleException,
    JetsonNanoEngineException,
    OutputModuleException,
    PostprocessingModuleException,
    PreprocessingModuleException,
    RaspberryPiEngineException,
)
from .generic import UnknownException
from .input import (
    EmptyFrameBufferException,
    InputException,
    InvalidInputDeviceException,
    InvalidInputException,
    InvalidInputPathException,
)
from .loader import (
    InvalidColorMapException,
    InvalidLabelMapException,
    InvalidLabelMapPathException,
    InvalidModelConfigException,
    InvalidModelException,
    InvalidModelPathException,
    LoaderException,
    UnsupportedModelFormatException,
)
from .logger import InvalidDebugFilePathException, LoggerException
from .output import (
    InvalidOutputDeviceException,
    InvalidOutputModuleException,
    InvalidOutputPathException,
    InvalidOutputTypeException,
    MalformedOutputException,
    OutputException,
)
from .postprocessor import (
    InvalidPostprocessorException,
    PostprocessingException,
    PostprocessorException,
)
from .predictor import (
    InvalidBoundTypeException,
    InvalidModelInputException,
    InvalidModelOutputException,
    PredictionException,
    PredictorException,
    UnsupportedModelArchitectureException,
)
from .preprocessor import (
    InvalidPreprocessorException,
    PreprocessingException,
    PreprocessorException,
)

__all__ = [
    "InvalidConfigException",
    "InvalidConfigPathException",
    "CPUEngineException",
    "EngineException",
    "InferenceModuleException",
    "InputModuleException",
    "JetsonNanoEngineException",
    "OutputModuleException",
    "PostprocessingModuleException",
    "PreprocessingModuleException",
    "RaspberryPiEngineException",
    "UnknownException",
    "EmptyFrameBufferException",
    "InputException",
    "InvalidInputDeviceException",
    "InvalidInputException",
    "InvalidInputPathException",
    "InvalidColorMapException",
    "InvalidLabelMapException",
    "InvalidLabelMapPathException",
    "InvalidModelConfigException",
    "InvalidModelException",
    "InvalidModelPathException",
    "LoaderException",
    "UnsupportedModelFormatException",
    "InvalidDebugFilePathException",
    "LoggerException",
    "InvalidOutputDeviceException",
    "InvalidOutputModuleException",
    "InvalidOutputPathException",
    "InvalidOutputTypeException",
    "MalformedOutputException",
    "OutputException",
    "InvalidPostprocessorException",
    "PostprocessingException",
    "PostprocessorException",
    "InvalidBoundTypeException",
    "InvalidModelInputException",
    "InvalidModelOutputException",
    "PredictionException",
    "PredictorException",
    "UnsupportedModelArchitectureException",
    "InvalidPreprocessorException",
    "PreprocessingException",
    "PreprocessorException",
]
