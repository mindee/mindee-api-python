from typing import Union

from mindee.parsing.common.string_dict import StringDict
from mindee.parsing.v2.base_field import BaseField, ListField, ObjectField, SimpleField


class InferenceFields(dict[str, Union[SimpleField, ObjectField, ListField]]):
    """Inference fields dict."""

    def __init__(self, raw_response: StringDict) -> None:
        super().__init__()
        for key, value in raw_response.items():
            field_obj = BaseField.create_field(value, 0)
            self[key] = field_obj

    def __getattr__(self, item):
        try:
            return self[item]
        except KeyError:
            raise AttributeError(item) from None
