#!/usr/bin/python3.7
# -*-coding:utf-8 -*-
"""
  ████
██    ██   Datature
  ██  ██   Powering Breakthrough AI
    ██

@File    :   loader.py
@Author  :   Wei Loon Cheng
@Version :   1.0
@Contact :   hello@datature.io
@License :   Apache License 2.0
@Desc    :   PyTorch Loader class.
"""

import torch
from abstract_loader import AbstractLoader


class Loader(AbstractLoader):

    """PyTorch Loader class."""

    def _load(self):
        """Load PyTorch model."""
        self.model = torch.load(self.model_path)
