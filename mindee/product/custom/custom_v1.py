from typing import List, Optional, TypeVar

from mindee.parsing.common import Inference, StringDict, clean_out_string, Page
from mindee.parsing.custom import ClassificationField, ListField
from mindee.product.custom.custom_v1_document import CustomV1Document
from mindee.product.custom.custom_v1_page import CustomV1Page


class CustomV1(Inference):
    """Custom document (API Builder) v1 inference results."""

    prediction: CustomV1Document
    pages: List[Page[CustomV1Page]]
    endpoint_name = "custom"
    endpoint_version = "1"

    def __init__(
        self,
        raw_prediction: StringDict
    ):
        """
        Custom document object.

        :param document_type: Document type
        :param api_prediction: Raw prediction from HTTP response
        :param input_source: Input object
        :param page_id: Page number for multi pages pdf input
        """
        super().__init__(raw_prediction)
        self.prediction = CustomV1Document(raw_prediction["prediction"])
        self.pages = []
        for page in raw_prediction["pages"]:
            self.pages.append(Page(CustomV1Page, page, page["id"], page["orientation"]))

    def _build_from_api_prediction(
        self, api_prediction: StringDict, page_id: Optional[int] = None
    ) -> None:
        """
        Build the document from an API response JSON.

        :param api_prediction: Raw prediction from HTTP response
        :param page_id: Page number for multi pages pdf input
        """
        self.fields = {}
        self.classifications = {}
        for field_name in api_prediction:
            field = api_prediction[field_name]
            # Only classifications have the 'value' attribute.
            if "value" in field:
                self.classifications[field_name] = ClassificationField(prediction=field)
            # Only value lists have the 'values' attribute.
            elif "values" in field:
                field["page_id"] = page_id
                self.fields[field_name] = ListField(prediction=field, page_id=page_id)

TypeCustomV1 = TypeVar("TypeCustomV1", bound=CustomV1)
