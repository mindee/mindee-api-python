from typing import Optional

from mindee.parsing.common.string_dict import StringDict
from mindee.parsing.v2.field.inference_result_fields import InferenceResultFields
from mindee.parsing.v2.inference_result_options import InferenceResultOptions


class InferenceResult:
    """Inference result info."""

    fields: InferenceResultFields
    """Fields contained in the inference."""
    options: Optional[InferenceResultOptions]
    """Potential options retrieved alongside the inference."""

    def __init__(self, raw_response: StringDict) -> None:
        self.fields = InferenceResultFields(raw_response["fields"])
        self.options = (
            InferenceResultOptions(raw_response["options"])
            if raw_response.get("options")
            else None
        )

    def __str__(self) -> str:
        out_str = f"\n\nFields\n======{self.fields}"
        if self.options:
            out_str += f"\n\nOptions\n====={self.options}"
        return out_str
