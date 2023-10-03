from typing import Dict, Optional

from mindee.parsing.common import Prediction, StringDict, clean_out_string
from mindee.parsing.custom import ClassificationField, ListField


class CustomV1Document(Prediction):
    """Custom V1 document prediction results."""

    fields: Dict[str, ListField]
    """Dictionary of all fields in the document"""
    classifications: Dict[str, ClassificationField]
    """Dictionary of all classifications in the document"""

    def __init__(self, raw_prediction: StringDict, page_id: Optional[int] = None):
        """
        Custom document object.

        :param raw_prediction: Dictionary containing the JSON document response
        """
        self._build_from_raw_prediction(raw_prediction, page_id=page_id)

    def _build_from_raw_prediction(
        self, raw_prediction: StringDict, page_id: Optional[int] = None
    ) -> None:
        """
        Build the document from an API response JSON.

        :param raw_prediction: Raw prediction from HTTP response
        :param page_id: Page number for multi pages pdf input
        """
        self.fields = {}
        self.classifications = {}
        for field_name, field_contents in raw_prediction.items():
            if "value" in field_contents:
                self.classifications[field_name] = ClassificationField(field_contents)
            # Only value lists have the 'values' attribute.
            elif "values" in field_contents:
                self.fields[field_name] = ListField(field_contents, page_id=page_id)

    def __str__(self) -> str:
        out_str = ""
        for classification_name, classification_value in self.classifications.items():
            out_str += f":{classification_name}: {classification_value}\n"
        for field_name, field_value in self.fields.items():
            out_str += f":{field_name}: {field_value}\n"
        return clean_out_string(out_str).rstrip()
