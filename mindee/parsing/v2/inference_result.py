from mindee.parsing.common.string_dict import StringDict
from mindee.parsing.v2.inference_fields import InferenceFields
from mindee.parsing.v2.inference_options import InferenceOptions


class InferenceResult:
    """Inference result info."""

    fields: InferenceFields
    """Fields contained in the inference."""
    options: InferenceOptions
    """Potential options retrieved alongside the inference."""

    def __init__(self, json_response: StringDict) -> None:
        self.fields = InferenceFields(json_response["fields"])
        self.options = InferenceOptions(json_response["options"])

    def __str__(self) -> str:
        str_fields = ""
        for field_key, field_value in self.fields.items():
            str_fields += f"  :{field_key}: {field_value}\n"
        return f":fields: {str_fields}\n" f"options: {self.options}\n"
