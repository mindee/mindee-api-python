from typing import Optional, TypeVar

from mindee.parsing.common.string_dict import StringDict


class Prediction:
    """Base Prediction class."""

    def __init__(self, raw_prediction: StringDict, page_id: Optional[int] = None):
        """
        Base prediction.

        :param raw_prediction: a json-equivalent dictionary containing prediction results.
        :param page_id: an optional page number for page-level predictions.
        """


TypePrediction = TypeVar("TypePrediction", bound=Prediction)
