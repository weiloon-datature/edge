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
@Desc    :   Raspberry Pi engine class.
"""

from abstract_engine import AbstractEngine
from common.constants import Timers
from common.exceptions import RaspberryPiEngineException
from common.logger import Logger
from common.profiling import timing


class Engine(AbstractEngine):

    """Raspberry Pi engine class."""

    def run(self):
        """Run Raspberry Pi engine.

        Raises:
            RaspberryPiEngineException: If engine fails to run.
        """
        if not self._inference_engine or not self._input_module:
            raise RaspberryPiEngineException(
                "Inference engine and input module must be initialized!")

        # Process input from input module
        self._input_module.run()
        try:
            while True:
                self._loop()

                if self._input_module.stopped:
                    break
                for output in self._output_modules:
                    if output.stopped:
                        break
        except KeyboardInterrupt:
            Logger.warning("Keyboard interrupt detected!")
            Logger.info("Stopping Datature Edge...")
        except Exception as exc:
            raise RaspberryPiEngineException(exc) from exc
        finally:
            self._cleanup()

    @timing(Timers.PERF_COUNTER)
    def _loop(self):
        """CPU engine loop."""
        # Get input from input module
        self._input_module.load_data(self._assets)

        # Get preprocessed input from preprocessors modules
        for preprocessor in self._preprocessor_modules:
            preprocessor.run(self._assets)

        # Get predictions from inference engine
        self._inference_engine.run(self._assets)

        # Get postprocessed predictions from postprocessors modules
        for postprocessor in self._postprocessor_modules:
            postprocessor.run(self._assets)

        # Send output to output modules
        for output in self._output_modules:
            output.run(self._assets)
