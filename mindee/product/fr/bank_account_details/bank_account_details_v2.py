from typing import List

from mindee.parsing.common import Inference, Page, StringDict
from mindee.product.fr.bank_account_details.bank_account_details_v2_document import (
    BankAccountDetailsV2Document,
)


class BankAccountDetailsV2(Inference):
    """Inference prediction for Bank Account Details, API version 2."""

    prediction: BankAccountDetailsV2Document
    """Document-level prediction."""
    pages: List[Page[BankAccountDetailsV2Document]]
    """Page-level prediction(s)."""
    endpoint_name = "bank_account_details"
    """Name of the endpoint."""
    endpoint_version = "2"
    """Version of the endpoint."""

    def __init__(self, raw_prediction: StringDict):
        """
        Bank Account Details v2 inference.

        :param raw_prediction: Raw prediction from the HTTP response.
        """
        super().__init__(raw_prediction)

        self.prediction = BankAccountDetailsV2Document(raw_prediction["prediction"])
        self.pages = []
        for page in raw_prediction["pages"]:
            try:
                page_production = page["prediction"]
            except KeyError:
                continue
            if page_production:
                self.pages.append(Page(BankAccountDetailsV2Document, page))
