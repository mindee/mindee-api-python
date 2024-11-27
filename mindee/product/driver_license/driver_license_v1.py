from typing import List

from mindee.parsing.common.inference import Inference
from mindee.parsing.common.page import Page
from mindee.parsing.common.string_dict import StringDict
from mindee.product.driver_license.driver_license_v1_document import (
    DriverLicenseV1Document,
)


class DriverLicenseV1(Inference):
    """Driver License API version 1 inference prediction."""

    prediction: DriverLicenseV1Document
    """Document-level prediction."""
    pages: List[Page[DriverLicenseV1Document]]
    """Page-level prediction(s)."""
    endpoint_name = "driver_license"
    """Name of the endpoint."""
    endpoint_version = "1"
    """Version of the endpoint."""

    def __init__(self, raw_prediction: StringDict):
        """
        Driver License v1 inference.

        :param raw_prediction: Raw prediction from the HTTP response.
        """
        super().__init__(raw_prediction)

        self.prediction = DriverLicenseV1Document(raw_prediction["prediction"])
        self.pages = []
        for page in raw_prediction["pages"]:
            try:
                page_prediction = page["prediction"]
            except KeyError:
                continue
            if page_prediction:
                self.pages.append(Page(DriverLicenseV1Document, page))
