from typing import Dict, Union

from mindee.parsing.common import Prediction, StringDict, clean_out_string
from mindee.parsing.custom import GeneratedListField
from mindee.parsing.standard.text import StringField


class GeneratedV1Document(Prediction):
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
        for field_name, field_contents in raw_prediction.items():
            if isinstance(field_contents, list):
                self.fields[field_name] = GeneratedListField(field_contents)
            else:
                self.fields[field_name] = StringField(field_contents)

    def __str__(self) -> str:
        out_str = ""
        for field_name, field_value in self.fields.items():
            out_str += f":{field_name}: {field_value}\n"
        return clean_out_string(out_str)
