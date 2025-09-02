from mindee.parsing.common.string_dict import StringDict
from mindee.parsing.v2.inference_active_options import InferenceActiveOptions
from mindee.parsing.v2.inference_file import InferenceFile
from mindee.parsing.v2.inference_model import InferenceModel
from mindee.parsing.v2.inference_result import InferenceResult


class Inference:
    """Inference object for a V2 API return."""

    id: str
    """ID of the inference."""
    model: InferenceModel
    """Model info for the inference."""
    file: InferenceFile
    """File info for the inference."""
    result: InferenceResult
    """Result of the inference."""
    active_options: InferenceActiveOptions
    """Active options for the inference."""

    def __init__(self, raw_response: StringDict):
        self.id = raw_response["id"]
        self.model = InferenceModel(raw_response["model"])
        self.file = InferenceFile(raw_response["file"])
        self.result = InferenceResult(raw_response["result"])
        self.active_options = InferenceActiveOptions(raw_response["active_options"])

    def __str__(self) -> str:
        return (
            f"Inference\n#########"
            f"\n{self.model}"
            f"\n\n{self.file}"
            f"\n\n{self.active_options}"
            f"\n\n{self.result}\n"
        )
