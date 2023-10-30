from typing import List

from mindee.parsing.common import Inference, Page, StringDict
from mindee.product.material_certificate.material_certificate_v1_document import (
    MaterialCertificateV1Document,
)


class MaterialCertificateV1(Inference):
    """Inference prediction for Material Certificate, API version 1."""

    prediction: MaterialCertificateV1Document
    """Document-level prediction."""
    pages: List[Page[MaterialCertificateV1Document]]
    """Page-level prediction(s)."""
    endpoint_name = "material_certificate"
    """Name of the endpoint."""
    endpoint_version = "1"
    """Version of the endpoint."""

    def __init__(self, raw_prediction: StringDict):
        """
        Material Certificate v1 inference.

        :param raw_prediction: Raw prediction from the HTTP response.
        """
        super().__init__(raw_prediction)

        self.prediction = MaterialCertificateV1Document(raw_prediction["prediction"])
        self.pages = []
        for page in raw_prediction["pages"]:
            self.pages.append(Page(MaterialCertificateV1Document, page))
