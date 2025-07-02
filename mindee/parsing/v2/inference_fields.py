from typing import Union

from mindee.parsing.v2.base_field import ListField, ObjectField, SimpleField


class InferenceFields(dict[str, Union[ObjectField, ListField, SimpleField]]):
    """Inference fields dict."""
