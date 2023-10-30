from typing import List

from mindee.parsing.common import Inference, Page, StringDict
from mindee.product.receipt.receipt_v5_document import ReceiptV5Document


class ReceiptV5(Inference):
    """Inference prediction for Receipt, API version 5."""

    prediction: ReceiptV5Document
    """Document-level prediction."""
    pages: List[Page[ReceiptV5Document]]
    """Page-level prediction(s)."""
    endpoint_name = "expense_receipts"
    """Name of the endpoint."""
    endpoint_version = "5"
    """Version of the endpoint."""

    def __init__(self, raw_prediction: StringDict):
        """
        Receipt v5 inference.

        :param raw_prediction: Raw prediction from the HTTP response.
        """
        super().__init__(raw_prediction)

        self.prediction = ReceiptV5Document(raw_prediction["prediction"])
        self.pages = []
        for page in raw_prediction["pages"]:
            self.pages.append(Page(ReceiptV5Document, page))
