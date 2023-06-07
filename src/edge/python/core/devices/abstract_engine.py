#!/usr/bin/python3.7
# -*-coding:utf-8 -*-
"""
  ████
██    ██   Datature
  ██  ██   Powering Breakthrough AI
    ██

@File    :   abstract_engine.py
@Author  :   Wei Loon Cheng
@Version :   1.0
@Contact :   hello@datature.io
@License :   Apache License 2.0
@Desc    :   Abstract engine class.
"""

import time
from abc import ABC, abstractmethod
from importlib import import_module

from abstract_input import AbstractInput
from abstract_output import AbstractOutput
from abstract_postprocessor import AbstractPostprocessor
from abstract_preprocessor import AbstractPreprocessor
from common.config import CONFIG
from common.exceptions import (
    InferenceModuleException,
    InputModuleException,
    OutputModuleException,
    PostprocessingModuleException,
    PreprocessingModuleException,
)
from common.logger import Logger
from core.components.inference import InferenceEngine


class AbstractEngine(ABC):

    """Abstract engine class."""

    def __init__(self, config=False):
        """Initialize engine."""
        self._inference_engine = None
        self._input_module = None
        self._preprocessor_modules = []
        self._postprocessor_modules = []
        self._output_modules = []

        if config:
            self._device = CONFIG["device"]

            Logger.debug("Loading inference engine...")
            try:
                self._inference_engine = InferenceEngine()
            except Exception as exc:
                raise InferenceModuleException(
                    f"Failed to load inference engine: {exc}") from exc
            Logger.debug("Loaded inference engine!")

            self._assets = {
                "category_index": self._inference_engine.loader.category_index,
                "color_map": self._inference_engine.loader.color_map
            }

            try:
                if "input" in CONFIG["blocks"]:
                    Logger.debug("Loading input module...")
                    self._input_module = import_module(
                        f"core.devices.{self._device}.modules.input"
                        f".{CONFIG['blocks']['input']['name']}.module").Input(
                            **CONFIG["blocks"]["input"])
                    Logger.debug("Loaded input modules!")
            except Exception as exc:
                raise InputModuleException(
                    f"Failed to load input module: {exc}") from exc

            try:
                if "preprocessors" in CONFIG["blocks"]:
                    Logger.debug("Loading preprocessor module(s)...")
                    for preprocessor in CONFIG["blocks"]["preprocessors"][
                            "modules"]:
                        module_key = list(preprocessor.keys())[-1]
                        kwargs = preprocessor[module_key]
                        kwargs["name"] = module_key
                        self._preprocessor_modules.append(
                            import_module(
                                f"core.components.data.preprocessors"
                                f".{module_key}.module").Preprocessor(
                                    **kwargs))
                    Logger.debug("Loaded preprocessor module(s)!")
            except Exception as exc:
                raise PreprocessingModuleException(
                    f"Failed to load preprocessor module(s): {exc}") from exc

            try:
                if "postprocessors" in CONFIG["blocks"]:
                    Logger.debug("Loading postprocessor module(s)...")
                    for postprocessor in CONFIG["blocks"]["postprocessors"][
                            "modules"]:
                        module_key = list(postprocessor.keys())[-1]
                        kwargs = postprocessor[module_key]
                        kwargs["name"] = module_key
                        self._postprocessor_modules.append(
                            import_module(
                                f"core.components.data.postprocessors"
                                f".{module_key}.module").Postprocessor(
                                    **kwargs))
                    Logger.debug("Loaded postprocessor module(s)!")
            except Exception as exc:
                raise PostprocessingModuleException(
                    f"Failed to load postprocessor module(s): {exc}") from exc

            try:
                if "output" in CONFIG["blocks"]:
                    Logger.debug("Loading output module(s)...")
                    for output in CONFIG["blocks"]["output"]["modules"]:
                        module_key = list(output.keys())[-1]
                        kwargs = output[module_key]
                        kwargs["name"] = module_key
                        self._output_modules.append(
                            import_module(
                                f"core.devices.{self._device}.modules.output"
                                f".{module_key}.module").Output(**kwargs))
                    Logger.debug("Loaded output module(s)!")
            except Exception as exc:
                raise OutputModuleException(
                    f"Failed to load output module(s): {exc}") from exc

    @abstractmethod
    def run(self):
        """Run engine.

        Raises:
            NotImplementedError
        """
        raise NotImplementedError

    def set_input_module(self, input_module):
        """Set input module.

        Args:
            input_module (Input): Input module.

        Raises:
            InputModuleException: If input module is not of type Input.
        """
        if not isinstance(input_module, AbstractInput):
            raise InputModuleException(
                "Input module must be of type AbstractInput.")
        self._input_module = input_module

    def add_preprocess_module(self, preprocessor_module):
        """Add preprocessor module.

        Args:
            preprocessor_module (Preprocessor): Preprocessor module.

        Raises:
            PreprocessingModuleException:
                If preprocessor module is not of type Preprocessor.
        """
        if not isinstance(preprocessor_module, AbstractPreprocessor):
            raise PreprocessingModuleException(
                "Preprocessor module must be of type AbstractPreprocessor.")
        self._preprocessor_modules.append(preprocessor_module)

    def add_postprocess_module(self, postprocessor_module):
        """Add postprocessor module.

        Args:
            postprocessor_module (Postprocessor): Postprocessor module.

        Raises:
            PostprocessingModuleException:
                If postprocessor module is not of type Postprocessor.
        """
        if not isinstance(postprocessor_module, AbstractPostprocessor):
            raise PostprocessingModuleException(
                "Postprocessor module must be of type AbstractPostprocessor.")
        self._postprocessor_modules.append(postprocessor_module)

    def add_output_module(self, output_module):
        """Add output module.

        Args:
            output_module (Output): Output module.

        Raises:
            OutputModuleException: If output module is not of type Output.
        """
        if not isinstance(output_module, AbstractOutput):
            raise OutputModuleException(
                "Output module must be of type AbstractOutput.")
        self._output_modules.append(output_module)

    def add_inference_engine(self, inference_engine):
        """Add inference engine.

        Args:
            inference_engine (InferenceEngine): Inference engine.

        Raises:
            InferenceModuleException:
                If inference engine is not of type InferenceEngine.
        """
        if not isinstance(inference_engine, InferenceEngine):
            raise InferenceModuleException(
                "Inference engine must be of type InferenceEngine.")
        self._inference_engine = inference_engine

    def summary(self):
        """Get engine pipeline summary.

        Returns:
            dict: Engine pipeline summary.
        """
        return {
            "input_modules":
            self._input_module.name if self._input_module else None,
            "preprocessor_modules":
            [module.name for module in self._preprocessor_modules],
            "inference_engine": [
                self._inference_engine.predictor.detection_type,
                self._inference_engine.loader.model_format,
                self._inference_engine.loader.model_architecture,
            ] if self._inference_engine else None,
            "postprocessor_modules":
            [module.name for module in self._postprocessor_modules],
            "output_modules": [module.name for module in self._output_modules],
        }

    def compile(self):
        """Check if engine pipeline is valid.

        Raises:
            NotImplementedError: If not implemented.
        """
        # TODO: Implement self._inputs, self._outputs for all input,
        # TODO: preprocessing, postprocessing, output modules,
        # TODO: and loader and predictor modules in inference engine.
        # TODO: Then, sequentially check if the output of one module
        # TODO: matches the input of the next module.
        raise NotImplementedError

    def _cleanup(self):
        """Clean up I/O modules."""
        Logger.debug("Cleaning up I/O modules...")
        self._input_module.stop()
        for output in self._output_modules:
            output.stop()
        time.sleep(1)
