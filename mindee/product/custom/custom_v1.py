from typing import List, TypeVar

from mindee.parsing.common import Inference, Page, StringDict
from mindee.product.custom.custom_v1_document import CustomV1Document
from mindee.product.custom.custom_v1_page import CustomV1Page


class CustomV1(Inference):
    """Custom document (API Builder) v1 inference results."""

    prediction: CustomV1Document
    pages: List[Page[CustomV1Page]]
    endpoint_name = "custom"
    endpoint_version = "1"

    def __init__(self, raw_prediction: StringDict) -> None:
        """
        Custom document object.

        :param document_type: Document type
        :param raw_prediction: Raw prediction from HTTP response
        :param input_source: Input object
        :param page_id: Page number for multi pages pdf input
        """
        super().__init__(raw_prediction)
        self.prediction = CustomV1Document(raw_prediction["prediction"])
        self.pages = []
        for page in raw_prediction["pages"]:
            self.pages.append(Page(CustomV1Page, page, page["id"], page["orientation"]))


TypeCustomV1 = TypeVar("TypeCustomV1", bound=CustomV1)
