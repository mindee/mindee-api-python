from typing import List

from mindee.parsing.common import Inference
from mindee.parsing.common.page import Page
from mindee.parsing.common.string_dict import StringDict
from mindee.product.receipt.receipt_v4_document import ReceiptV4Document


class ReceiptV4(Inference):
    """Inference prediction for Receipt, API version 4."""

    prediction: ReceiptV4Document
    pages: List[Page[ReceiptV4Document]]
    endpoint_name = "expense_receipts"
    """The endpoint's name"""
    endpoint_version = "4"
    """The endpoint's version"""

    def __init__(
        self,
        raw_prediction: StringDict,
    ) -> None:
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
