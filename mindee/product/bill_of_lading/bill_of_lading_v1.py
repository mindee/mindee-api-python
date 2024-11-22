from typing import List

from mindee.parsing.common.inference import Inference
from mindee.parsing.common.page import Page
from mindee.parsing.common.string_dict import StringDict
from mindee.product.bill_of_lading.bill_of_lading_v1_document import (
    BillOfLadingV1Document,
)


class BillOfLadingV1(Inference):
    """Bill of Lading API version 1 inference prediction."""

    prediction: BillOfLadingV1Document
    """Document-level prediction."""
    pages: List[Page[BillOfLadingV1Document]]
    """Page-level prediction(s)."""
    endpoint_name = "bill_of_lading"
    """Name of the endpoint."""
    endpoint_version = "1"
    """Version of the endpoint."""

    def __init__(self, raw_prediction: StringDict):
        """
        Bill of Lading v1 inference.

        :param raw_prediction: Raw prediction from the HTTP response.
        """
        super().__init__(raw_prediction)

        self.prediction = BillOfLadingV1Document(raw_prediction["prediction"])
        self.pages = []
        for page in raw_prediction["pages"]:
            try:
                page_prediction = page["prediction"]
            except KeyError:
                continue
            if page_prediction:
                self.pages.append(Page(BillOfLadingV1Document, page))
