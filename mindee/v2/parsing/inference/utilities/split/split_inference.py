from mindee.parsing.common.string_dict import StringDict
from mindee.v2.parsing.inference.base_inference import BaseInference
from mindee.v2.parsing.inference.utilities.split.split_result import SplitResult


class SplitInference(BaseInference):
    """Split inference result."""

    result: SplitResult
    """Result of a split inference."""
    _slug: str = "split"
    """Slug of the endpoint."""

    def __init__(self, raw_response: StringDict) -> None:
        super().__init__(raw_response)
        self.result = SplitResult(raw_response["result"])

    def __str__(self) -> str:
        return f"Inference\n#########\n{self.model}\n{self.file}\n{self.result}\n"
