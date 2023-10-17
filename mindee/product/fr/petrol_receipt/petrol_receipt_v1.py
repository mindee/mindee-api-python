from typing import List

from mindee.parsing.common import Inference, Page, StringDict
from mindee.product.fr.petrol_receipt.petrol_receipt_v1_document import (
    PetrolReceiptV1Document,
)


class PetrolReceiptV1(Inference):
    """Inference prediction for Petrol Receipt, API version 1."""

    prediction: PetrolReceiptV1Document
    """Document-level prediction."""
    pages: List[Page[PetrolReceiptV1Document]]
    """Page-level prediction(s)."""
    endpoint_name = "petrol_receipts"
    """Name of the endpoint."""
    endpoint_version = "1"
    """Version of the endpoint."""

    def __init__(self, raw_prediction: StringDict):
        """
        Petrol Receipt v1 inference.

        :param raw_prediction: Raw prediction from the HTTP response.
        """
        super().__init__(raw_prediction)

        self.prediction = PetrolReceiptV1Document(raw_prediction["prediction"])
        self.pages = []
        for page in raw_prediction["pages"]:
            self.pages.append(Page(PetrolReceiptV1Document, page))
