from typing import Dict, List, Union

from mindee.parsing.common import Prediction, StringDict, clean_out_string
from mindee.parsing.custom import GeneratedListField
from mindee.parsing.standard.text import StringField


class GeneratedV1Prediction(Prediction):
    """Generated V1 document prediction results."""

    fields: Dict[str, Union[GeneratedListField, StringField]]
    """Dictionary of all fields in the document"""

    def __init__(self, raw_prediction: StringDict) -> None:
        """
        Generated document.

        :param raw_prediction: Dictionary containing the JSON document response
        """
        super().__init__(raw_prediction)
        self.fields = {}

    def __str__(self) -> str:
        out_str = ""
        for field_name, field_value in self.fields.items():
            out_str += f":{field_name}: {field_value}\n"
        return clean_out_string(out_str)

    def get_single_fields(self) -> Dict[str, StringField]:
        """Returns a dictionary of all fields that aren't a collection."""
        single_fields = {}
        for field_name, field_value in self.fields.items():
            if isinstance(field_value, StringField):
                single_fields[field_name] = field_value
        return single_fields

    def get_multiple_fields(self) -> Dict[str, GeneratedListField]:
        """Returns a dictionary of all collection fields."""
        multiple_fields = {}
        for field_name, field_value in self.fields.items():
            if isinstance(field_value, GeneratedListField):
                multiple_fields[field_name] = field_value
        return multiple_fields

    def list_field_names(self) -> List[str]:
        """Lists names of all field keys."""
        return list(self.fields.keys())
            