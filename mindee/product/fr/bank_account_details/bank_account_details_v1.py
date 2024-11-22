from typing import List

from mindee.parsing.common.inference import Inference
from mindee.parsing.common.page import Page
from mindee.parsing.common.string_dict import StringDict
from mindee.product.fr.bank_account_details.bank_account_details_v1_document import (
    BankAccountDetailsV1Document,
)


class BankAccountDetailsV1(Inference):
    """Bank Account Details API version 1 inference prediction."""

    prediction: BankAccountDetailsV1Document
    """Document-level prediction."""
    pages: List[Page[BankAccountDetailsV1Document]]
    """Page-level prediction(s)."""
    endpoint_name = "bank_account_details"
    """Name of the endpoint."""
    endpoint_version = "1"
    """Version of the endpoint."""

    def __init__(self, raw_prediction: StringDict):
        """
        Bank Account Details v1 inference.

        :param raw_prediction: Raw prediction from the HTTP response.
        """
        super().__init__(raw_prediction)

        self.prediction = BankAccountDetailsV1Document(raw_prediction["prediction"])
        self.pages = []
        for page in raw_prediction["pages"]:
            try:
                page_prediction = page["prediction"]
            except KeyError:
                continue
            if page_prediction:
                self.pages.append(Page(BankAccountDetailsV1Document, page))
