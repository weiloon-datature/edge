#!/usr/bin/python3.7
# -*-coding:utf-8 -*-
"""
  ████
██    ██   Datature
  ██  ██   Powering Breakthrough AI
    ██

@File    :   predictor.py
@Author  :   Wei Loon Cheng
@Version :   1.0
@Contact :   hello@datature.io
@License :   Apache License 2.0
@Desc    :   Predictor exceptions.
"""


class PredictorException(Exception):

    """Base class for exceptions in the predictor module."""


class UnsupportedModelArchitectureException(PredictorException):

    """Exception raised for unsupported model architecture."""


class InvalidModelInputException(PredictorException):

    """Exception raised for errors in the input model."""


class PredictionException(PredictorException):

    """Exception raised for errors in the prediction."""


class InvalidModelOutputException(PredictorException):

    """Exception raised for errors in the model output."""


class InvalidBoundTypeException(PredictorException):

    """Exception raised for errors in the bound type."""
