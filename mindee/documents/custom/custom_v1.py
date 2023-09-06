from typing import Dict, Optional, TypeVar

from mindee.documents.base import Document, TypeApiPrediction, clean_out_string
from mindee.documents.custom.custom_v1_fields import ClassificationField, ListField


class CustomV1(Document):
    """Custom document (API Builder) v1 prediction results."""

    fields: Dict[str, ListField]
    """Dictionary of all fields in the document"""
    classifications: Dict[str, ClassificationField]
    """Dictionary of all classifications in the document"""

    def __init__(
        self,
        document_type: str,
        api_prediction: TypeApiPrediction,
        input_source=None,
        page_n: Optional[int] = None,
    ):
        """
        Custom document object.

        :param document_type: Document type
        :param api_prediction: Raw prediction from HTTP response
        :param input_source: Input object
        :param page_n: Page number for multi pages pdf input
        """
        super().__init__(
            input_source=input_source,
            document_type=document_type,
            api_prediction=api_prediction,
            page_n=page_n,
        )
        self._build_from_api_prediction(api_prediction["prediction"], page_n=page_n)

    def _build_from_api_prediction(
        self, api_prediction: TypeApiPrediction, page_n: Optional[int] = None
    ) -> None:
        """
        Build the document from an API response JSON.

        :param api_prediction: Raw prediction from HTTP response
        :param page_n: Page number for multi pages pdf input
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
                field["page_n"] = page_n
                self.fields[field_name] = ListField(prediction=field, page_n=page_n)

    def __str__(self) -> str:
        custom_doc_str = f"{self.type} V1 Prediction"
        custom_doc_str += "\n" + "=" * len(custom_doc_str)
        custom_doc_str += f"\n:Filename: {self.filename or ''}\n"

        for class_name, class_info in self.classifications.items():
            custom_doc_str += f":{class_name}: {class_info}\n"
        for field_name, field_info in self.fields.items():
            custom_doc_str += f":{field_name}: {field_info}\n"
        return clean_out_string(custom_doc_str)


TypeCustomV1 = TypeVar("TypeCustomV1", bound=CustomV1)
