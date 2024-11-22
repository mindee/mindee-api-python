from typing import List

from mindee.parsing.common.inference import Inference
from mindee.parsing.common.page import Page
from mindee.parsing.common.string_dict import StringDict
from mindee.product.financial_document.financial_document_v1_document import (
    FinancialDocumentV1Document,
)


class FinancialDocumentV1(Inference):
    """Financial Document API version 1 inference prediction."""

    prediction: FinancialDocumentV1Document
    """Document-level prediction."""
    pages: List[Page[FinancialDocumentV1Document]]
    """Page-level prediction(s)."""
    endpoint_name = "financial_document"
    """Name of the endpoint."""
    endpoint_version = "1"
    """Version of the endpoint."""

    def __init__(self, raw_prediction: StringDict):
        """
        Financial Document v1 inference.

        :param raw_prediction: Raw prediction from the HTTP response.
        """
        super().__init__(raw_prediction)

        self.prediction = FinancialDocumentV1Document(raw_prediction["prediction"])
        self.pages = []
        for page in raw_prediction["pages"]:
            try:
                page_prediction = page["prediction"]
            except KeyError:
                continue
            if page_prediction:
                self.pages.append(Page(FinancialDocumentV1Document, page))
