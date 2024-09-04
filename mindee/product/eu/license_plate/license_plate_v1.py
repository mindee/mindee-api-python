from typing import List

from mindee.parsing.common import Inference, Page, StringDict
from mindee.product.eu.license_plate.license_plate_v1_document import (
    LicensePlateV1Document,
)


class LicensePlateV1(Inference):
    """License Plate API version 1 inference prediction."""

    prediction: LicensePlateV1Document
    """Document-level prediction."""
    pages: List[Page[LicensePlateV1Document]]
    """Page-level prediction(s)."""
    endpoint_name = "license_plates"
    """Name of the endpoint."""
    endpoint_version = "1"
    """Version of the endpoint."""

    def __init__(self, raw_prediction: StringDict):
        """
        License Plate v1 inference.

        :param raw_prediction: Raw prediction from the HTTP response.
        """
        super().__init__(raw_prediction)

        self.prediction = LicensePlateV1Document(raw_prediction["prediction"])
        self.pages = []
        for page in raw_prediction["pages"]:
            try:
                page_prediction = page["prediction"]
            except KeyError:
                continue
            if page_prediction:
                self.pages.append(Page(LicensePlateV1Document, page))
