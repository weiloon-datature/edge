import os

## Set Configuration File Path
os.environ["DATATURE_EDGE_PYTHON_CONFIG"] = "./samples/python/config.yaml"

from common.logger import Logger
from core.devices import DeviceEngine

try:
    device_engine = DeviceEngine(config=True)
    device_engine.run()
except Exception as exc:  # pylint: disable=broad-except
    Logger.error(f"{exc.__class__.__name__}: {exc}")
