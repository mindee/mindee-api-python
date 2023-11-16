from typing import Dict, List

from mindee.parsing.common import Prediction, StringDict, clean_out_string
from mindee.parsing.custom import ClassificationFieldV2, ListFieldV2
from mindee.parsing.custom.line_items import CustomLineV2


class CustomV2Document(Prediction):
    """Custom V2 document prediction results."""

    fields: Dict[str, ListFieldV2]
    """Dictionary of all fields in the document"""
    classifications: Dict[str, ClassificationFieldV2]
    """Dictionary of all classifications in the document"""

    def __init__(self, raw_prediction: StringDict) -> None:
        """
        Custom document.

        :param raw_prediction: Dictionary containing the JSON document response
        """
        self.fields = {}
        self.classifications = {}
        for field_name, field_contents in raw_prediction.items():
            if "value" in field_contents:
                self.classifications[field_name] = ClassificationFieldV2(field_contents)
            # Only value lists have the 'values' attribute.
            elif "values" in field_contents:
                self.fields[field_name] = ListFieldV2(field_contents)

    def columns_to_line_items(
        self,
        anchor_names: List[str],
        field_names: List[str],
        height_tolerance: float = 0.01,
    ) -> List[CustomLineV2]:
        """
        Order column fields into line items.

        :param anchor_names: list of possible anchor fields.
        :param field_names: list of all column fields.
        :param height_tolerance: height tolerance to apply to lines.
        """
        return CustomLineV2.get_line_items(
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
