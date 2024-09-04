from typing import List

from mindee.parsing.common import Inference, Page, StringDict
from mindee.product.international_id.international_id_v1_document import (
    InternationalIdV1Document,
)


class InternationalIdV1(Inference):
    """Inference prediction for International ID, API version 1."""

    prediction: InternationalIdV1Document
    """Document-level prediction."""
    pages: List[Page[InternationalIdV1Document]]
    """Page-level prediction(s)."""
    endpoint_name = "international_id"
    """Name of the endpoint."""
    endpoint_version = "1"
    """Version of the endpoint."""

    def __init__(self, raw_prediction: StringDict):
        """
        International ID v1 inference.

        :param raw_prediction: Raw prediction from the HTTP response.
        """
        super().__init__(raw_prediction)

        self.prediction = InternationalIdV1Document(raw_prediction["prediction"])
        self.pages = []
        for page in raw_prediction["pages"]:
            try:
                page_prediction = page["prediction"]
            except KeyError:
                continue
            if page_prediction:
                self.pages.append(Page(InternationalIdV1Document, page))
