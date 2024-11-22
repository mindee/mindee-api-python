from typing import Dict, Union

from mindee.parsing.common.string_dict import StringDict
from mindee.parsing.generated.generated_list import GeneratedListField
from mindee.parsing.generated.generated_object import (
    GeneratedObjectField,
    is_generated_object,
)
from mindee.parsing.standard.text import StringField
from mindee.product.generated.generated_v1_prediction import GeneratedV1Prediction


class GeneratedV1Document(GeneratedV1Prediction):
    """Generated V1 document prediction results."""

    fields: Dict[str, Union[GeneratedListField, StringField, GeneratedObjectField]]
    """Dictionary of all fields in the document"""

    def __init__(self, raw_prediction: StringDict) -> None:
        """
        Generated document.

        :param raw_prediction: Dictionary containing the JSON document response
        """
        super().__init__(raw_prediction)
        for field_name, field_contents in raw_prediction.items():
            if isinstance(field_contents, list):
                self.fields[field_name] = GeneratedListField(field_contents)
            elif isinstance(field_contents, dict) and is_generated_object(
                field_contents
            ):
                self.fields[field_name] = GeneratedObjectField(field_contents)
            else:
                field_contents_str = field_contents
                if (
                    "value" in field_contents_str
                    and field_contents_str["value"] is not None
                ):
                    field_contents_str["value"] = str(
                        field_contents_str["value"]
                    )  # str coercion for numbers
                self.fields[field_name] = StringField(field_contents_str)
