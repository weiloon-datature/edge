#!/usr/bin/python3.7
# -*-coding:utf-8 -*-
"""
  ████
██    ██   Datature
  ██  ██   Powering Breakthrough AI
    ██

@File    :   main.py
@Author  :   Wei Loon Cheng
@Version :   1.0
@Contact :   hello@datature.io
@License :   Apache License 2.0
@Desc    :   Main entry point for Datature Edge Engine.
"""

import traceback

from common.logger import Logger
from core.devices import DeviceEngine
from graceful_shutdown import ShutdownProtection
from prettyprinter import pformat

if __name__ == "__main__":
    Logger.info("Starting Datature Edge Engine...")
    with ShutdownProtection(4) as protected_block:
        try:
            device_engine = DeviceEngine(config=True)
            Logger.info(pformat(device_engine.summary()))
            device_engine.run()
        except Exception as exc:  # pylint: disable=broad-except
            Logger.error(f"{exc.__class__.__name__}: {exc}")
            Logger.debug(traceback.format_exc())
        finally:
            Logger.info("Datature Edge Engine stopped!")
