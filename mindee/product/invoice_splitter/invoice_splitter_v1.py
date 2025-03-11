from typing import List

from mindee.parsing.common.inference import Inference
from mindee.parsing.common.page import Page
from mindee.parsing.common.string_dict import StringDict
from mindee.product.invoice_splitter.invoice_splitter_v1_document import (
    InvoiceSplitterV1Document,
)


class InvoiceSplitterV1(Inference):
    """Invoice Splitter API version 1 inference prediction."""

    prediction: InvoiceSplitterV1Document
    """Document-level prediction."""
    pages: List[Page[InvoiceSplitterV1Document]]
    """Page-level prediction(s)."""
    endpoint_name = "invoice_splitter"
    """Name of the endpoint."""
    endpoint_version = "1"
    """Version of the endpoint."""

    def __init__(self, raw_prediction: StringDict):
        """
        Invoice Splitter v1 inference.

        :param raw_prediction: Raw prediction from the HTTP response.
        """
        super().__init__(raw_prediction)

        self.prediction = InvoiceSplitterV1Document(raw_prediction["prediction"])
        self.pages = []
        for page in raw_prediction["pages"]:
            try:
                page_prediction = page["prediction"]
            except KeyError:
                continue
            if page_prediction:
                self.pages.append(Page(InvoiceSplitterV1Document, page))
