from typing import Dict, List, Optional

from mindee.parsing.common import Prediction, StringDict, clean_out_string
from mindee.parsing.custom import ListFieldV1
from mindee.parsing.custom.line_items import CustomLineV1, get_line_items


class CustomV1Page(Prediction):
    """Custom V1 page prediction results."""

    fields: Dict[str, ListFieldV1]
    """Dictionary of all fields in the document"""

    def __init__(self, raw_prediction: StringDict, page_id: Optional[int]) -> None:
        """
        Custom document object.

        :param raw_prediction: Dictionary containing the JSON document response
        """
        self.fields = {}
        for field_name, field_contents in raw_prediction.items():
            self.fields[field_name] = ListFieldV1(field_contents, page_id=page_id)

    def columns_to_line_items(
        self,
        anchor_names: List[str],
        field_names: List[str],
        height_tolerance: float = 0.01,
    ) -> List[CustomLineV1]:
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
        for field_name, field_value in self.fields.items():
            out_str += f":{field_name}: {field_value}\n"
        return clean_out_string(out_str)
