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
@Desc    :   Module for Raspberry Pi PiCamera input.
"""

import sys
import time
from threading import Thread

from abstract_input import AbstractInput
from common.constants import timestamp
from common.exceptions import InvalidInputException
from common.logger import Logger

try:
    from picamera import PiCamera
    from picamera.array import PiRGBArray
except ImportError:
    Logger.error("picamera module not found. Please install it.")
    sys.exit(1)


class Input(AbstractInput):

    """PiCamera input class for Raspberry Pi."""

    def __init__(self, **kwargs):
        """Initialize the PiCamera input.

        Raises:
            InvalidInputException: If video stream cannot be opened
                or input device is not found.
        """
        self.device = None
        self.frame_size = [None, None]
        self.fps = None
        self.max_buffer = -1
        super().__init__(**kwargs)
        self._frame = None
        self._frame_id = None
        self._cwnd = self.max_buffer if self.max_buffer > 0 else 100
        self._frame_buffer = 0

        # Initialize the camera and stream
        Logger.debug("Warming up camera...")
        self._camera = PiCamera()
        self._camera.resolution = self.frame_size if self.frame_size else (640,
                                                                           480)
        self._camera.framerate = self.fps if self.fps else 32
        self._camera.CAPTURE_TIMEOUT = 60
        self._raw_capture = PiRGBArray(
            self._camera,
            size=self.frame_size if self.frame_size else (640, 480))
        time.sleep(0.1)
        Logger.info("Camera ready!")

    def run(self):
        """Start the thread to read frames from the video stream."""
        Thread(target=self.update, args=(), daemon=True).start()
        return self

    def update(self):
        """Continuously grab frames from the stream."""
        # Keep looping infinitely until the thread is stopped
        Logger.debug("Grabbing frames...")
        try:
            for frame in self._camera.capture_continuous(self._raw_capture,
                                                         format="bgr",
                                                         use_video_port=True):
                if self.stopped:
                    return

                if frame.array is None:
                    Logger.warning("No frame grabbed!")
                    time.sleep(1)
                    continue

                # AIMD algorithm for congestion control
                self._frame_buffer += 1
                if self._frame_buffer < self._cwnd:
                    self._frame_id = timestamp()
                    self._frame = frame.array
                    self._cwnd = self._cwnd + 1 / self._cwnd
                    self._frame_buffer -= 1
                else:
                    Logger.debug("Throttling frames...")
                    self._cwnd //= 2
                self._raw_capture.truncate(0)
                self._raw_capture.seek(0)
        except Exception as exc:
            raise InvalidInputException(exc) from exc

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
        Logger.debug("Cleaning up camera resources...")
        self.stopped = True
        time.sleep(1)
        self._raw_capture.close()
        self._camera.close()
