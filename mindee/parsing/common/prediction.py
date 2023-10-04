from typing import TypeVar


class Prediction:
    """Base Prediction class."""


TypePrediction = TypeVar("TypePrediction", bound=Prediction)
