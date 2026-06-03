from mindee.parsing.common import StringDict
from mindee.v2.error.mindee_api_v2_error import MindeeAPIV2Error
from mindee.v2.parsing.inference.field.list_field import ListField
from mindee.v2.parsing.inference.field.object_field import ObjectField
from mindee.v2.parsing.inference.field.simple_field import SimpleField


def parse_field(raw_response: StringDict, indent_level: int = 0):
    """The central parser function to be injected down the tree."""
    if "value" in raw_response:
        return SimpleField(raw_response, indent_level)
    if "items" in raw_response:
        return ListField(raw_response, parse_field, indent_level)
    if "fields" in raw_response:
        return ObjectField(raw_response, parse_field, indent_level)

    raise MindeeAPIV2Error(f"Unrecognized field type in {raw_response}.")
