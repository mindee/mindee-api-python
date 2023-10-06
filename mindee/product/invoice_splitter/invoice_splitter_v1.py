from typing import List

from mindee.parsing.common import Inference, Page, StringDict
from mindee.product.invoice_splitter.invoice_splitter_v1_document import (
    InvoiceSplitterV1Document,
)


class InvoiceSplitterV1(Inference):
    """Inference prediction for Invoice Splitter, API version 1."""

    prediction: InvoiceSplitterV1Document
    """Document-level prediction."""
    pages: List[Page[InvoiceSplitterV1Document]]
    """Page-level prediction(s)."""
    endpoint_name = "invoice_splitter"
    """Name of the endpoint."""
    endpoint_version = "1"
    """Version of the endpoint."""

    def __init__(self, raw_prediction: StringDict) -> None:
        """
        Invoice Splitter v1 inference.

        :param raw_prediction: Raw prediction from the HTTP response.
        """
        super().__init__(raw_prediction)
        self.prediction = InvoiceSplitterV1Document(raw_prediction["prediction"])
        self.pages = []
        for page in raw_prediction["pages"]:
            self.pages.append(Page(InvoiceSplitterV1Document, page))
