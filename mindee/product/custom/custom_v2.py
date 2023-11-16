from typing import List

from mindee.parsing.common import Inference, Page, StringDict
from mindee.product.custom.custom_v2_document import CustomV2Document
from mindee.product.custom.custom_v2_page import CustomV2Page


class CustomV2(Inference):
    """Custom document (API Builder) v2 inference results."""

    prediction: CustomV2Document
    """Document-level prediction."""
    pages: List[Page[CustomV2Page]]
    """Page-level prediction(s)."""
    endpoint_name = "custom"
    """Name of the endpoint."""
    endpoint_version = "1"
    """Version of the endpoint. Note: corresponds to the version of the custom **model**, not the API itself."""

    def __init__(self, raw_prediction: StringDict) -> None:
        """
        Custom v2 inference.

        :param raw_prediction: Raw prediction from the HTTP response.
        """
        super().__init__(raw_prediction)
        self.prediction = CustomV2Document(raw_prediction["prediction"])
        self.pages = []
        for page in raw_prediction["pages"]:
            self.pages.append(Page(CustomV2Page, page))
