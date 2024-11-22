from typing import List

from mindee.parsing.common.inference import Inference
from mindee.parsing.common.page import Page
from mindee.parsing.common.string_dict import StringDict
from mindee.product.invoice.invoice_v4_document import (
    InvoiceV4Document,
)


class InvoiceV4(Inference):
    """Invoice API version 4 inference prediction."""

    prediction: InvoiceV4Document
    """Document-level prediction."""
    pages: List[Page[InvoiceV4Document]]
    """Page-level prediction(s)."""
    endpoint_name = "invoices"
    """Name of the endpoint."""
    endpoint_version = "4"
    """Version of the endpoint."""

    def __init__(self, raw_prediction: StringDict):
        """
        Invoice v4 inference.

        :param raw_prediction: Raw prediction from the HTTP response.
        """
        super().__init__(raw_prediction)

        self.prediction = InvoiceV4Document(raw_prediction["prediction"])
        self.pages = []
        for page in raw_prediction["pages"]:
            try:
                page_prediction = page["prediction"]
            except KeyError:
                continue
            if page_prediction:
                self.pages.append(Page(InvoiceV4Document, page))
