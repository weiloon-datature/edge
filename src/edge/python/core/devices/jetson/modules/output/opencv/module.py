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
@Desc    :   Module for Jetson OpenCV output.
"""

import cv2
from abstract_output import AbstractOutput
from common.exceptions import InvalidOutputPathException, InvalidOutputTypeException
from common.logger import Logger


class Output(AbstractOutput):

    """Jetson OpenCV output class."""

    def __init__(self, **kwargs):
        """Initialize Jetson OpenCV output class."""
        self.type = ""
        self.output_path = ""
        self.window_name = ""
        self.frame_size = [-1, -1]
        self.fps = 30
        self._video_frames = []
        super().__init__(**kwargs)

        if self.type == "video_save":
            self._frame_count = 0
            self._total_frame_count = 0
            self._video_writer = cv2.VideoWriter(
                self.output_path,
                cv2.VideoWriter_fourcc(*"mp4v"),
                self.fps,
                tuple(self.frame_size),
            )

    def run(self, assets):
        """Run Jetson OpenCV output module.

        Args:
            assets: Dictionary of assets.

        Raises:
            InvalidOutputTypeException: Unsupported or no output type.
        """
        frame = assets["output_frame"]
        if self.type == "image_show":
            self._image_show(frame)
        elif self.type == "image_save":
            self._image_save(frame)
        elif self.type == "video_show":
            self._video_show(frame)
        elif self.type == "video_save":
            self._total_frame_count = assets["total_frame_count"]
            self._video_save(frame, assets["frame_id"])
        else:
            raise InvalidOutputTypeException("Unsupported output type!")

    def _image_show(self, frame):
        """Show image on screen.

        Args:
            frame: Frame to be displayed.
        """
        window_name = self.window_name if self.window_name else "Datature Edge"
        cv2.imshow(window_name, frame)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        self.stop()

    def _image_save(self, frame):
        """Save image to disk.

        Args:
            frame: Frame to be saved.
        """
        if not hasattr(self, "output_path"):
            raise InvalidOutputPathException("No output path provided!")
        Logger.info(f"Saving output to {self.output_path}...")
        cv2.imwrite(self.output_path, frame)

    def _video_show(self, frame):
        """Show video on screen.

        Args:
            frame: Frame to be displayed.
        """
        window_name = self.window_name if self.window_name else "Datature Edge"
        cv2.imshow(window_name, frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            Logger.warning("Closing output display window...")
            cv2.destroyAllWindows()
            self.stop()

    def _video_save(self, frame, frame_id):
        """Save video to disk.

        Args:
            frame: Frame to be saved.
        """
        if not hasattr(self, "output_path"):
            raise InvalidOutputPathException("No output path provided!")
        Logger.debug(
            f"Adding output frame {frame_id} to {self.output_path}...")
        self._video_writer.write(frame)
        self._frame_count += 1

        if self._frame_count == self._total_frame_count:
            Logger.info(f"Saving output video {self.output_path}...")
            self._video_writer.release()
            self.stop()
