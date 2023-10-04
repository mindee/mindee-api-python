from typing import TypeVar


class Prediction:
    """Base Prediction class."""

    def __init__(self, *args) -> None:
        pass


TypePrediction = TypeVar("TypePrediction", bound=Prediction)
