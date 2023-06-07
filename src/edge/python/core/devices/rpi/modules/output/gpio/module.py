#!/usr/bin/python3.7
# -*-coding:utf-8 -*-
"""
  ████
██    ██   Datature
  ██  ██   Powering Breakthrough AI
    ██

@File    :   module.py
@Author  :   Wei Loon Cheng
@Version :   1.0
@Contact :   hello@datature.io
@License :   Apache License 2.0
@Desc    :   Module for Raspberry Pi GPIO output.
"""

try:
    from RPi import GPIO
except ImportError as exc:
    raise ImportError("GPIO module not available on this system!") from exc

from abstract_output import AbstractOutput
from common.exceptions import InvalidOutputDeviceException


class Output(AbstractOutput):

    """Raspberry Pi GPIO output class."""

    def __init__(self, **kwargs):
        """Initialize Raspberry Pi GPIO output class."""
        self.input_pin = -1
        self.output_pin = -1
        super().__init__(**kwargs)
        GPIO.setmode(GPIO.BOARD)
        if self.input_pin > 0:
            GPIO.setup(self.input_pin, GPIO.IN)
        else:
            raise InvalidOutputDeviceException("Input pin not set!")
        if self.output_pin > 0:
            GPIO.setup(self.output_pin, GPIO.OUT, initial=GPIO.LOW)
        else:
            raise InvalidOutputDeviceException("Output pin not set!")

    def run(self, assets):
        """Run Raspberry Pi GPIO output.

        Args:
            assets: Dictionary of assets.
        """
        # TODO: Implement logic to turn on/off GPIO pins
