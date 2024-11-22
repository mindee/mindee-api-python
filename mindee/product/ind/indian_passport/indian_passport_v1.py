from typing import List

from mindee.parsing.common.inference import Inference
from mindee.parsing.common.page import Page
from mindee.parsing.common.string_dict import StringDict
from mindee.product.ind.indian_passport.indian_passport_v1_document import (
    IndianPassportV1Document,
)


class IndianPassportV1(Inference):
    """Passport - India API version 1 inference prediction."""

    prediction: IndianPassportV1Document
    """Document-level prediction."""
    pages: List[Page[IndianPassportV1Document]]
    """Page-level prediction(s)."""
    endpoint_name = "ind_passport"
    """Name of the endpoint."""
    endpoint_version = "1"
    """Version of the endpoint."""

    def __init__(self, raw_prediction: StringDict):
        """
        Passport - India v1 inference.

        :param raw_prediction: Raw prediction from the HTTP response.
        """
        super().__init__(raw_prediction)

        self.prediction = IndianPassportV1Document(raw_prediction["prediction"])
        self.pages = []
        for page in raw_prediction["pages"]:
            try:
                page_prediction = page["prediction"]
            except KeyError:
                continue
            if page_prediction:
                self.pages.append(Page(IndianPassportV1Document, page))
