from typing import Any, Dict

from mindee.parsing.common import Inference
from mindee.parsing.common.page import Page
from mindee.product.receipt.receipt_v4_document import (
    ReceiptV4Document,
    TypeReceiptV4Document,
)


class ReceiptV4(Inference):
    """Receipt v4 prediction results."""

    endpoint_name = "expense_receipts"
    """The endpoint's name"""
    endpoint_version = "4"
    """The endpoint's version"""

    def __init__(
        self,
        raw_prediction: Dict[str, Any],
    ):
        """
        Receipt document.

        :param raw_prediction: Raw prediction from HTTP response
        :param page_id: Page number for multi pages pdf input
        """
        super().__init__(raw_prediction=raw_prediction)
        self.prediction = ReceiptV4Document(raw_prediction["prediction"])
        self.pages = []
        for page in raw_prediction["pages"]:
            self.pages.append(
                Page[ReceiptV4Document](
                    ReceiptV4Document,
                    page,
                    page_id=page["id"],
                    orientation=page["orientation"],
                )
            )
