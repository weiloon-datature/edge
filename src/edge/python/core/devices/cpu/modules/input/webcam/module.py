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
@Desc    :   Module for CPU webcam input.
"""

import time
from threading import Thread

import cv2
from abstract_input import AbstractInput
from common.constants import timestamp
from common.exceptions import InvalidInputException
from common.logger import Logger


class Input(AbstractInput):

    """Webcam input class for CPU."""

    def __init__(self, **kwargs):
        """Initialize the webcam input.

        Raises:
            InvalidInputException: If video stream cannot be opened
                or input device is not found.
        """
        self.device = None
        self.frame_size = [None, None]
        self.max_buffer = -1
        super().__init__(**kwargs)
        self._frame = None
        self._frame_id = None
        self._cwnd = self.max_buffer if self.max_buffer > 0 else 100
        self._frame_buffer = 0

        Logger.debug("Warming up camera...")
        self._stream = cv2.VideoCapture(self.device)
        if not self._stream.isOpened():
            raise InvalidInputException("Could not open video stream!")
        self._stream.set(cv2.CAP_PROP_FRAME_WIDTH, self.frame_size[0])
        self._stream.set(cv2.CAP_PROP_FRAME_HEIGHT, self.frame_size[1])
        time.sleep(0.1)
        Logger.info("Camera ready!")

    def run(self):
        """Start the thread to read frames from the video stream."""
        Thread(target=self.update, args=(), daemon=True).start()
        return self

    def update(self):
        """Continuously grab frames from the stream."""
        Logger.debug("Grabbing frames...")
        while True:
            if self.stopped:
                return

            (grabbed, frame) = self._stream.read()
            if not grabbed:
                Logger.warning("No frame grabbed!")
                time.sleep(1)
                continue

            # AIMD algorithm for congestion control
            self._frame_buffer += 1
            if self._frame_buffer < self._cwnd:
                self._frame_id = timestamp()
                self._frame = frame
                self._cwnd = self._cwnd + 1 / self._cwnd
                self._frame_buffer -= 1
            else:
                Logger.debug("Throttling frames...")
                self._cwnd //= 2

    def load_data(self, assets):
        """Load input data.

        Args:
            assets: Dictionary of assets.
        """
        while self._frame is None:
            time.sleep(0.1)
        assets["frame_id"] = self._frame_id
        assets["orig_frame"] = self._frame
        assets["orig_shape"] = assets["orig_frame"].shape
        assets["input_frame"] = assets["orig_frame"].copy()

    def stop(self):
        """Stop the frame reading thread."""
        Logger.debug("Releasing camera resources...")
        self.stopped = True
        time.sleep(1)
        self._stream.release()
