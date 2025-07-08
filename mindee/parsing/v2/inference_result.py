from typing import Optional

from mindee.parsing.common.string_dict import StringDict
from mindee.parsing.v2.base_field import InferenceFields
from mindee.parsing.v2.inference_options import InferenceOptions


class InferenceResult:
    """Inference result info."""

    fields: InferenceFields
    """Fields contained in the inference."""
    options: Optional[InferenceOptions]
    """Potential options retrieved alongside the inference."""

    def __init__(self, raw_response: StringDict) -> None:
        self.fields = InferenceFields(raw_response["fields"])
        self.options = (
            InferenceOptions(raw_response["options"])
            if raw_response.get("options")
            else None
        )

    def __str__(self) -> str:
        out_str = f":fields: {self.fields}"
        if self.options:
            out_str += f"\n:options: {self.options}"
        return out_str
