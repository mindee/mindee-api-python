from typing import Dict, List

from mindee.parsing.common.prediction import Prediction
from mindee.parsing.common.string_dict import StringDict
from mindee.parsing.common.summary_helper import clean_out_string
from mindee.parsing.custom.classification import ClassificationField
from mindee.parsing.custom.line_items import CustomLine, get_line_items
from mindee.parsing.custom.list import ListField


class CustomV1Document(Prediction):
    """Custom V1 document prediction results."""

    fields: Dict[str, ListField]
    """Dictionary of all fields in the document"""
    classifications: Dict[str, ClassificationField]
    """Dictionary of all classifications in the document"""

    def __init__(self, raw_prediction: StringDict) -> None:
        """
        Custom document.

        :param raw_prediction: Dictionary containing the JSON document response
        """
        super().__init__(raw_prediction)
        self.fields = {}
        self.classifications = {}
        for field_name, field_contents in raw_prediction.items():
            if "value" in field_contents:
                self.classifications[field_name] = ClassificationField(field_contents)
            # Only value lists have the 'values' attribute.
            elif "values" in field_contents:
                self.fields[field_name] = ListField(field_contents)

    def columns_to_line_items(
        self,
        anchor_names: List[str],
        field_names: List[str],
        height_tolerance: float = 0.01,
    ) -> List[CustomLine]:
        """
        Order column fields into line items.

        :param anchor_names: list of possible anchor fields.
        :param field_names: list of all column fields.
        :param height_tolerance: height tolerance to apply to lines.
        """
        return get_line_items(
            anchor_names,
            field_names,
            self.fields,
            height_tolerance,
        )

    def __str__(self) -> str:
        out_str = ""
        for classification_name, classification_value in self.classifications.items():
            out_str += f":{classification_name}: {classification_value}\n"
        for field_name, field_value in self.fields.items():
            out_str += f":{field_name}: {field_value}\n"
        return clean_out_string(out_str)
