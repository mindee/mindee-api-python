from typing import Dict, Optional, Union

from mindee.parsing.common import Prediction, StringDict
from mindee.parsing.custom import GeneratedListField
from mindee.parsing.custom.generated_object import GeneratedObjectField
from mindee.parsing.standard.text import StringField


class GeneratedV1Page(Prediction):
    """Generated V1 page prediction results."""

    fields: Dict[str, Union[GeneratedListField, StringField, GeneratedObjectField]]
    """Dictionary of all fields in the document"""

    def __init__(self, raw_prediction: StringDict, page_id: Optional[int]) -> None:
        """
        Generated document object.

        :param raw_prediction: Dictionary containing the JSON document response
        """
        super().__init__(raw_prediction, page_id)
        for field_name, field_contents in raw_prediction.items():
            if isinstance(field_contents, list):
                self.fields[field_name] = GeneratedListField(field_contents, page_id)
            elif isinstance(field_contents, dict):
                self.fields[field_name] = GeneratedObjectField(field_contents, page_id)
            else:
                self.fields[field_name] = StringField(field_contents, page_id=page_id)
