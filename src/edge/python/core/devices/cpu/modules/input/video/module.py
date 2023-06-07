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
@Desc    :   Module for CPU video input.
"""

import time
from threading import Thread

import cv2
import numpy as np
from abstract_input import AbstractInput
from common.exceptions import InvalidInputPathException
from common.logger import Logger


class Input(AbstractInput):

    """CPU video input class."""

    def __init__(self, **kwargs):
        """Initialize CPU video input class."""
        self.frame_size = [None, None]
        self.video_path = ""
        super().__init__(**kwargs)
        self._frames = []
        self._frame_ids = []
        self._frame = None
        self._frame_index = 0

        self._video = cv2.VideoCapture(self.video_path)
        if not self._video.isOpened():
            raise InvalidInputPathException("Could not open video stream!")
        self._total_frame_count = int(self._video.get(
            cv2.CAP_PROP_FRAME_COUNT))

    def run(self):
        """Start the thread to read frames from the video file."""
        Thread(target=self.update, args=(), daemon=True).start()
        return self

    def update(self):
        """Continuously grab frames from the video file."""
        Logger.debug("Grabbing frames...")

        count = 0
        ret = True

        while True:
            (ret, frame) = self._video.read()
            if not ret:
                return
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            self._frame_ids.append(f"{self.video_path}_{count}")
            self._frames.append(np.array(frame))
            self.frame_size = frame.shape

            count += 1

    def load_data(self, assets):
        """Load input data.

        Args:
            assets: Dictionary of assets.
        """
        if self._frame_index == self._total_frame_count - 1:
            self.stop()
        while len(self._frames) < self._frame_index + 1:
            time.sleep(0.1)

        assets["frame_id"] = self._frame_ids[self._frame_index]
        assets["orig_frame"] = self._frames[self._frame_index]
        assets["orig_shape"] = assets["orig_frame"].shape
        assets["input_frame"] = assets["orig_frame"].copy()
        assets["total_frame_count"] = self._total_frame_count

        self._frame_index += 1
        return assets

    def stop(self):
        """Stop CPU image input."""
        self.stopped = True
