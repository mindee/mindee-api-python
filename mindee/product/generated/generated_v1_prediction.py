import re
from typing import Dict, List, Union

from mindee.parsing.common.prediction import Prediction
from mindee.parsing.common.string_dict import StringDict
from mindee.parsing.common.summary_helper import clean_out_string
from mindee.parsing.generated.generated_list import GeneratedListField
from mindee.parsing.generated.generated_object import GeneratedObjectField
from mindee.parsing.standard.text import StringField


class GeneratedV1Prediction(Prediction):
    """Generated V1 document prediction results."""

    fields: Dict[str, Union[GeneratedListField, StringField, GeneratedObjectField]]
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
        pattern = re.compile(r"^(\n*[  ]*)( {2}):")
        for field_name, field_value in self.fields.items():
            str_value = ""
            if (
                isinstance(field_value, GeneratedListField)
                and len(field_value.values) > 0
            ):
                if isinstance(field_value.values[0], GeneratedObjectField):
                    str_value += re.sub(
                        pattern, r"\1* :", f"{field_value.values[0]._str_level(1)}"
                    )
                else:
                    str_value += re.sub(pattern, r"\1* :", f"{field_value.values[0]}\n")
                for sub_value in field_value.values[1:]:
                    if isinstance(sub_value, GeneratedObjectField):
                        str_value += re.sub(pattern, r"\1* :", sub_value._str_level(1))
                    else:
                        str_value += f" { ' ' * (len(field_name)+2)}{sub_value}\n"
                str_value = str_value.rstrip()
            else:
                str_value = str(field_value)
            out_str += f":{field_name}: {str_value}\n"
        return clean_out_string(out_str)

    def get_single_fields(self) -> Dict[str, StringField]:
        """Returns a dictionary of all fields that aren't a collection."""
        single_fields = {}
        for field_name, field_value in self.fields.items():
            if isinstance(field_value, StringField):
                single_fields[field_name] = field_value
        return single_fields

    def get_list_fields(self) -> Dict[str, GeneratedListField]:
        """Returns a dictionary of all list-like fields."""
        list_fields = {}
        for field_name, field_value in self.fields.items():
            if isinstance(field_value, GeneratedListField):
                list_fields[field_name] = field_value
        return list_fields

    def get_object_fields(self) -> Dict[str, GeneratedObjectField]:
        """Returns a dictionary of all object-like fields."""
        object_fields = {}
        for field_name, field_value in self.fields.items():
            if isinstance(field_value, GeneratedObjectField):
                object_fields[field_name] = field_value
        return object_fields

    def list_field_names(self) -> List[str]:
        """Lists names of all top-level field keys."""
        return list(self.fields.keys())
