from typing import Optional

from mindee.parsing.common.string_dict import StringDict
from mindee.parsing.v2.inference_file import InferenceFile
from mindee.parsing.v2.inference_model import InferenceModel
from mindee.parsing.v2.inference_result import InferenceResult


class Inference:
    """Inference object for a V2 API return."""

    model: InferenceModel
    """Model info for the inference."""
    file: InferenceFile
    """File info for the inference."""
    result: InferenceResult
    """Result of the inference."""
    id: Optional[str]
    """ID of the inference."""

    def __init__(self, raw_response: StringDict):
        self.model = InferenceModel(raw_response["model"])
        self.file = InferenceFile(raw_response["file"])
        self.result = InferenceResult(raw_response["result"])
        self.id = raw_response["id"] if "id" in raw_response else None

    def __str__(self) -> str:
        return (
            f"Inference\n#########\n"
            f"{self.model}\n\n"
            f"{self.file}"
            f"{self.result}\n"
        )
