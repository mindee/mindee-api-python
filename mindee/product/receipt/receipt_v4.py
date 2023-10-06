from typing import List

from mindee.parsing.common import Inference, Page, StringDict
from mindee.product.receipt.receipt_v4_document import ReceiptV4Document


class ReceiptV4(Inference):
    """Inference prediction for Receipt, API version 4."""

    prediction: ReceiptV4Document
    """Document-level prediction."""
    pages: List[Page[ReceiptV4Document]]
    """Page-level prediction(s)."""
    endpoint_name = "expense_receipts"
    """Name of the endpoint."""
    endpoint_version = "4"
    """Version of the endpoint."""

    def __init__(
        self,
        raw_prediction: StringDict,
    ) -> None:
        """
        Invoice Splitter v1 inference.

        :param raw_prediction: Raw prediction from the HTTP response.
        """
        super().__init__(raw_prediction=raw_prediction)
        self.prediction = ReceiptV4Document(raw_prediction["prediction"])
        self.pages = []
        for page in raw_prediction["pages"]:
            self.pages.append(Page(ReceiptV4Document, page))
