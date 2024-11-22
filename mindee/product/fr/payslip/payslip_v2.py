from typing import List

from mindee.parsing.common.inference import Inference
from mindee.parsing.common.page import Page
from mindee.parsing.common.string_dict import StringDict
from mindee.product.fr.payslip.payslip_v2_document import (
    PayslipV2Document,
)


class PayslipV2(Inference):
    """Payslip API version 2 inference prediction."""

    prediction: PayslipV2Document
    """Document-level prediction."""
    pages: List[Page[PayslipV2Document]]
    """Page-level prediction(s)."""
    endpoint_name = "payslip_fra"
    """Name of the endpoint."""
    endpoint_version = "2"
    """Version of the endpoint."""

    def __init__(self, raw_prediction: StringDict):
        """
        Payslip v2 inference.

        :param raw_prediction: Raw prediction from the HTTP response.
        """
        super().__init__(raw_prediction)

        self.prediction = PayslipV2Document(raw_prediction["prediction"])
        self.pages = []
        for page in raw_prediction["pages"]:
            try:
                page_prediction = page["prediction"]
            except KeyError:
                continue
            if page_prediction:
                self.pages.append(Page(PayslipV2Document, page))
