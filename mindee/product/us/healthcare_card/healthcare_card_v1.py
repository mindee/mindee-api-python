from typing import List

from mindee.parsing.common.inference import Inference
from mindee.parsing.common.page import Page
from mindee.parsing.common.string_dict import StringDict
from mindee.product.us.healthcare_card.healthcare_card_v1_document import (
    HealthcareCardV1Document,
)


class HealthcareCardV1(Inference):
    """Healthcare Card API version 1 inference prediction."""

    prediction: HealthcareCardV1Document
    """Document-level prediction."""
    pages: List[Page[HealthcareCardV1Document]]
    """Page-level prediction(s)."""
    endpoint_name = "us_healthcare_cards"
    """Name of the endpoint."""
    endpoint_version = "1"
    """Version of the endpoint."""

    def __init__(self, raw_prediction: StringDict):
        """
        Healthcare Card v1 inference.

        :param raw_prediction: Raw prediction from the HTTP response.
        """
        super().__init__(raw_prediction)

        self.prediction = HealthcareCardV1Document(raw_prediction["prediction"])
        self.pages = []
        for page in raw_prediction["pages"]:
            try:
                page_prediction = page["prediction"]
            except KeyError:
                continue
            if page_prediction:
                self.pages.append(Page(HealthcareCardV1Document, page))
