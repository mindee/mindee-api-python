from typing import List

from mindee.parsing.common.inference import Inference
from mindee.parsing.common.page import Page
from mindee.parsing.common.string_dict import StringDict
from mindee.product.generated.generated_v1_document import GeneratedV1Document
from mindee.product.generated.generated_v1_page import GeneratedV1Page


class GeneratedV1(Inference):
    """Generated API V1 inference results."""

    prediction: GeneratedV1Document
    """Document-level prediction."""
    pages: List[Page[GeneratedV1Page]]
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
        self.prediction = GeneratedV1Document(raw_prediction["prediction"])
        self.pages = []
        for page in raw_prediction["pages"]:
            if page["prediction"]:
                self.pages.append(Page(GeneratedV1Page, page))
