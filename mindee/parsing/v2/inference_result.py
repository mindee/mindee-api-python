from typing import Optional

from mindee.parsing.common.string_dict import StringDict
from mindee.parsing.v2.field.inference_result_fields import InferenceResultFields
from mindee.parsing.v2.raw_text import RawText


class InferenceResult:
    """Inference result info."""

    fields: InferenceResultFields
    """Fields contained in the inference."""
    raw_text: Optional[RawText] = None
    """Potential options retrieved alongside the inference."""

    def __init__(self, raw_response: StringDict) -> None:
        self.fields = InferenceResultFields(raw_response["fields"])
        if raw_response.get("raw_text"):
            self.raw_text = RawText(raw_response["raw_text"])

    def __str__(self) -> str:
        out_str = f"\n\nFields\n======{self.fields}"
        return out_str
