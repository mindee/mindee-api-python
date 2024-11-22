from typing import List

from mindee.parsing.common.inference import Inference
from mindee.parsing.common.page import Page
from mindee.parsing.common.string_dict import StringDict
from mindee.product.fr.energy_bill.energy_bill_v1_document import (
    EnergyBillV1Document,
)


class EnergyBillV1(Inference):
    """Energy Bill API version 1 inference prediction."""

    prediction: EnergyBillV1Document
    """Document-level prediction."""
    pages: List[Page[EnergyBillV1Document]]
    """Page-level prediction(s)."""
    endpoint_name = "energy_bill_fra"
    """Name of the endpoint."""
    endpoint_version = "1"
    """Version of the endpoint."""

    def __init__(self, raw_prediction: StringDict):
        """
        Energy Bill v1 inference.

        :param raw_prediction: Raw prediction from the HTTP response.
        """
        super().__init__(raw_prediction)

        self.prediction = EnergyBillV1Document(raw_prediction["prediction"])
        self.pages = []
        for page in raw_prediction["pages"]:
            try:
                page_prediction = page["prediction"]
            except KeyError:
                continue
            if page_prediction:
                self.pages.append(Page(EnergyBillV1Document, page))
