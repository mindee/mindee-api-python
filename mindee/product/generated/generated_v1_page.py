from typing import Dict, Optional, Union

from mindee.parsing.common import StringDict
from mindee.parsing.custom import GeneratedObjectField, is_generated_object
from mindee.parsing.custom.generated_list import GeneratedListField
from mindee.parsing.standard.text import StringField
from mindee.product.generated.generated_v1_prediction import GeneratedV1Prediction


class GeneratedV1Page(GeneratedV1Prediction):
    """Generated V1 page prediction results."""

    fields: Dict[str, Union[GeneratedListField, StringField, GeneratedObjectField]]
    """Dictionary of all fields in the document"""

    def __init__(
        self, raw_prediction: StringDict, page_id: Optional[int] = None
    ) -> None:
        """
        Generated document object.

        :param raw_prediction: Dictionary containing the JSON document response
        """
        super().__init__(raw_prediction)
        for field_name, field_contents in raw_prediction.items():
            if isinstance(field_contents, list):
                self.fields[field_name] = GeneratedListField(field_contents, page_id)
            elif isinstance(field_contents, dict) and is_generated_object(
                field_contents
            ):
                self.fields[field_name] = GeneratedObjectField(field_contents, page_id)
            else:
                self.fields[field_name] = StringField(field_contents, page_id=page_id)
