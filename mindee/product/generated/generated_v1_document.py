from typing import Dict, Union

from mindee.parsing.common import StringDict
from mindee.parsing.custom import GeneratedObjectField, is_generated_object
from mindee.parsing.custom.generated_list import GeneratedListField
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
                self.fields[field_name] = StringField(field_contents)
