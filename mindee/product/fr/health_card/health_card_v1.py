from typing import List

from mindee.parsing.common.inference import Inference
from mindee.parsing.common.page import Page
from mindee.parsing.common.string_dict import StringDict
from mindee.product.fr.health_card.health_card_v1_document import (
    HealthCardV1Document,
)


class HealthCardV1(Inference):
    """Health Card API version 1 inference prediction."""

    prediction: HealthCardV1Document
    """Document-level prediction."""
    pages: List[Page[HealthCardV1Document]]
    """Page-level prediction(s)."""
    endpoint_name = "french_healthcard"
    """Name of the endpoint."""
    endpoint_version = "1"
    """Version of the endpoint."""

    def __init__(self, raw_prediction: StringDict):
        """
        Health Card v1 inference.

        :param raw_prediction: Raw prediction from the HTTP response.
        """
        super().__init__(raw_prediction)

        self.prediction = HealthCardV1Document(raw_prediction["prediction"])
        self.pages = []
        for page in raw_prediction["pages"]:
            try:
                page_prediction = page["prediction"]
            except KeyError:
                continue
            if page_prediction:
                self.pages.append(Page(HealthCardV1Document, page))
