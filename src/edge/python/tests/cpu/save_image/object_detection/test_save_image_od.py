#!/usr/bin/python3.7
# -*-coding:utf-8 -*-
"""
  ████
██    ██   Datature
  ██  ██   Powering Breakthrough AI
    ██

@File    :   test_save_image_od.py
@Author  :   Wei Loon Cheng
@Version :   1.0
@Contact :   hello@datature.io
@License :   Apache License 2.0
@Desc    :   Object Detection Image Save test case.
"""

import os
import shutil
import traceback
from unittest import TestCase

from pytest import MonkeyPatch

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
monkeypatch = MonkeyPatch()


class TestSaveImageOD(TestCase):

    """Test Object Detection Image Save"""

    def test_onnx(self):
        """Test on ONNX model"""
        monkeypatch.setenv(
            "DATATURE_EDGE_PYTHON_CONFIG",
            os.path.join(CURRENT_DIR, "config/onnx_config.yaml"))
        self.exec()

    def test_tflite(self):
        """Test on TFLite model"""
        monkeypatch.setenv(
            "DATATURE_EDGE_PYTHON_CONFIG",
            os.path.join(CURRENT_DIR, "config/tflite_config.yaml"))
        self.exec()

    def exec(self):
        """Execute Datature Edge

        Raises:
            AssertionError: If image is not successfully saved.
        """
        from common.logger import Logger
        from core.devices import DeviceEngine

        if not os.path.exists(os.path.join(CURRENT_DIR, "out")):
            os.mkdir(os.path.join(CURRENT_DIR, "out"))

        try:
            device_engine = DeviceEngine()
            device_engine.run()
        except Exception as exc:  # pylint: disable=broad-except
            Logger.error(f"{exc.__class__.__name__}: {exc}")
            Logger.debug(traceback.format_exc())

        self.assertTrue(
            os.path.exists(os.path.join(CURRENT_DIR, "out/image.png")))

        os.unsetenv("DATATURE_EDGE_PYTHON_CONFIG")
        shutil.rmtree(os.path.join(CURRENT_DIR, "out"))
