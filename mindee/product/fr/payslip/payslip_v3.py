from typing import List

from mindee.parsing.common.inference import Inference
from mindee.parsing.common.page import Page
from mindee.parsing.common.string_dict import StringDict
from mindee.product.fr.payslip.payslip_v3_document import (
    PayslipV3Document,
)


class PayslipV3(Inference):
    """Payslip API version 3 inference prediction."""

    prediction: PayslipV3Document
    """Document-level prediction."""
    pages: List[Page[PayslipV3Document]]
    """Page-level prediction(s)."""
    endpoint_name = "payslip_fra"
    """Name of the endpoint."""
    endpoint_version = "3"
    """Version of the endpoint."""

    def __init__(self, raw_prediction: StringDict):
        """
        Payslip v3 inference.

        :param raw_prediction: Raw prediction from the HTTP response.
        """
        super().__init__(raw_prediction)

        self.prediction = PayslipV3Document(raw_prediction["prediction"])
        self.pages = []
        for page in raw_prediction["pages"]:
            try:
                page_prediction = page["prediction"]
            except KeyError:
                continue
            if page_prediction:
                self.pages.append(Page(PayslipV3Document, page))
