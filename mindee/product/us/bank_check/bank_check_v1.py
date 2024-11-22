from typing import List

from mindee.parsing.common.inference import Inference
from mindee.parsing.common.page import Page
from mindee.parsing.common.string_dict import StringDict
from mindee.product.us.bank_check.bank_check_v1_document import (
    BankCheckV1Document,
)
from mindee.product.us.bank_check.bank_check_v1_page import (
    BankCheckV1Page,
)


class BankCheckV1(Inference):
    """Bank Check API version 1 inference prediction."""

    prediction: BankCheckV1Document
    """Document-level prediction."""
    pages: List[Page[BankCheckV1Page]]
    """Page-level prediction(s)."""
    endpoint_name = "bank_check"
    """Name of the endpoint."""
    endpoint_version = "1"
    """Version of the endpoint."""

    def __init__(self, raw_prediction: StringDict):
        """
        Bank Check v1 inference.

        :param raw_prediction: Raw prediction from the HTTP response.
        """
        super().__init__(raw_prediction)

        self.prediction = BankCheckV1Document(raw_prediction["prediction"])
        self.pages = []
        for page in raw_prediction["pages"]:
            try:
                page_prediction = page["prediction"]
            except KeyError:
                continue
            if page_prediction:
                self.pages.append(Page(BankCheckV1Page, page))
