from typing import List

from mindee.parsing.common.inference import Inference
from mindee.parsing.common.page import Page
from mindee.parsing.common.string_dict import StringDict
from mindee.product.business_card.business_card_v1_document import (
    BusinessCardV1Document,
)


class BusinessCardV1(Inference):
    """Business Card API version 1 inference prediction."""

    prediction: BusinessCardV1Document
    """Document-level prediction."""
    pages: List[Page[BusinessCardV1Document]]
    """Page-level prediction(s)."""
    endpoint_name = "business_card"
    """Name of the endpoint."""
    endpoint_version = "1"
    """Version of the endpoint."""

    def __init__(self, raw_prediction: StringDict):
        """
        Business Card v1 inference.

        :param raw_prediction: Raw prediction from the HTTP response.
        """
        super().__init__(raw_prediction)

        self.prediction = BusinessCardV1Document(raw_prediction["prediction"])
        self.pages = []
        for page in raw_prediction["pages"]:
            try:
                page_prediction = page["prediction"]
            except KeyError:
                continue
            if page_prediction:
                self.pages.append(Page(BusinessCardV1Document, page))
