from typing import List

from mindee.parsing.common import Inference, Page, StringDict
from mindee.product.us.driver_license.driver_license_v1_document import (
    DriverLicenseV1Document,
)
from mindee.product.us.driver_license.driver_license_v1_page import DriverLicenseV1Page


class DriverLicenseV1(Inference):
    """Inference prediction for Driver License, API version 1."""

    prediction: DriverLicenseV1Document
    """Document-level prediction."""
    pages: List[Page[DriverLicenseV1Page]]
    """Page-level prediction(s)."""
    endpoint_name = "us_driver_license"
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
            self.pages.append(Page(DriverLicenseV1Page, page))
