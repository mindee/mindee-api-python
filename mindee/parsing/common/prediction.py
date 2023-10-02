from typing import Any, Dict, TypeVar


class Prediction:
    """Base Prediction class."""

    def __init__(self, *args):
        pass


TypePrediction = TypeVar("TypePrediction", bound=Prediction)
