from typing import List

from mindee.parsing.common.inference import Inference
from mindee.parsing.common.page import Page
from mindee.parsing.common.string_dict import StringDict
from mindee.product.custom.custom_v1_document import CustomV1Document
from mindee.product.custom.custom_v1_page import CustomV1Page


class CustomV1(Inference):
    """Custom document (API Builder) v1 inference results."""

    prediction: CustomV1Document
    """Document-level prediction."""
    pages: List[Page[CustomV1Page]]
    """Page-level prediction(s)."""
    endpoint_name = "custom"
    """Name of the endpoint (placeholder)."""
    endpoint_version = "1"
    """Version of the endpoint."""

    def __init__(self, raw_prediction: StringDict) -> None:
        """
        Invoice Splitter v1 inference.

        :param raw_prediction: Raw prediction from the HTTP response.
        """
        super().__init__(raw_prediction)
        self.prediction = CustomV1Document(raw_prediction["prediction"])
        self.pages = []
        for page in raw_prediction["pages"]:
            self.pages.append(Page(CustomV1Page, page))
