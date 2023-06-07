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
@Desc    :   Module for CPU active learning output.
"""

import csv
import time
import traceback
from threading import Thread

import cv2
import datature
from abstract_output import AbstractOutput
from common.exceptions import InvalidOutputPathException
from common.logger import Logger


class Output(AbstractOutput):

    """CPU active learning output class."""

    def __init__(self, **kwargs):
        """Initialise CPU active learning output class."""
        self.secret_key = ""
        self.frame_interval = 10
        self.upload_interval = 10
        self.asset_folder = ""
        self.prediction_folder = ""
        self._asset_groups = []
        self._frame_count = 0
        self._asset_buffer = []
        self._is_uploading = False
        self._upload_count = 0
        super().__init__(**kwargs)
        datature.secret_key = self.secret_key
        self._upload_session = datature.Asset.upload_session()

    def run(self, assets):
        """Run CPU active learning output.

        Args:
            assets: Dictionary of assets.
        """
        if self._is_uploading or assets["predictions"] == []:
            return
        if self._frame_count % self.frame_interval == 0:
            self._asset_buffer.append(
                (assets["frame_id"], assets["orig_frame"],
                 assets["predictions"]))
        if len(self._asset_buffer) == self.upload_interval:
            Thread(target=self._upload_assets,
                   args=(self._upload_count, assets["category_index"],
                         self._asset_buffer, self._frame_count),
                   daemon=True).start()
            self._asset_buffer = []
        self._frame_count += 1

    def _upload_assets(self, upload_count, category_index, asset_buffer,
                       frame_count):
        """Upload assets to Nexus using Datature SDK.

        Args:
            upload_count: Counter for total number of uploads performed.
            category_index: Dictionary of label classes.
            asset_buffer: List of assets to be uploaded, assets are in
                the form of a tuple of (frame_id, frame, predictions).
            frame_count: Counter for total number of frames processed.
        """
        self._is_uploading = True
        Logger.info(f"[Upload #{upload_count}] Starting upload...")
        start = time.time()
        self._write_assets_to_file(category_index, asset_buffer, frame_count)

        try:
            Logger.info(f"[Upload #{upload_count}] Uploading images...")
            op_link = self._upload_session.start(groups=self._asset_groups,
                                                 background=True)["op_link"]
            while datature.Operation.retrieve(op_link)["status"]["progress"][
                    "with_status"]["finished"] < len(asset_buffer):
                time.sleep(1)

            Logger.info(f"[Upload #{upload_count}] Uploading predictions...")
            op_link = datature.Annotation.upload(
                "csv_fourcorner",
                f"{self.prediction_folder}/preds_{frame_count}.csv",
                background=True)["op_link"]
            while datature.Operation.retrieve(op_link)["status"]["progress"][
                    "with_status"]["finished"] == 0:
                time.sleep(1)
        except Exception as exc:  # pylint: disable=broad-except
            Logger.warning(f"[Upload #{upload_count}] Upload failed: {exc}")
            Logger.debug(f"\n{traceback.format_exc()}")
            return

        end = time.time()
        Logger.info(
            f"[Upload #{upload_count}] Upload finished! Took {end - start}s")
        self._upload_count += 1
        self._is_uploading = False

    def _write_assets_to_file(self, category_index, asset_buffer, frame_count):
        """Save images as jpg and predictions as csv.

        Args:
            category_index: Dictionary of label classes.
            asset_buffer: List of assets to be uploaded, assets are in
                the form of a tuple of (frame_id, frame, predictions).
            frame_count: Counter for total number of frames processed.

        Raises:
            InvalidOutputPathException: If output path(s) to save
                images and predictions are invalid.
        """
        file_name = f"{self.prediction_folder}/preds_{frame_count}.csv"

        try:
            with open(file_name, 'w', encoding="utf-8") as f:
                writer = csv.writer(f)
                header = ["filename", "xmin", "ymin", "xmax", "ymax", "label"]
                writer.writerow(header)
                for img_id, image, prediction in asset_buffer:
                    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                    cv2.imwrite(f"{self.asset_folder}/{img_id}.jpg", image)
                    self._upload_session.add(
                        f"{self.asset_folder}/{img_id}.jpg")
                    for each_bbox, each_class, _ in zip(
                            prediction["boxes"], prediction["classes"],
                            prediction["scores"]):
                        label = str(category_index[int(each_class)]["name"])
                        row = [
                            f"{img_id}.jpg", each_bbox[1], each_bbox[0],
                            each_bbox[3], each_bbox[2], label
                        ]
                        writer.writerow(row)
        except Exception as exc:
            raise InvalidOutputPathException(exc) from exc
