from abc import ABC
from typing import TypeVar

from mindee.parsing.common.string_dict import StringDict
from mindee.parsing.v2.inference_file import InferenceFile
from mindee.parsing.v2.inference_model import InferenceModel


class BaseInference(ABC):
    """Base class for V2 inference objects."""

    model: InferenceModel
    """Model info for the inference."""
    file: InferenceFile
    """File info for the inference."""
    id: str
    """ID of the inference."""

    def __init__(self, raw_response: StringDict):
        self.id = raw_response["id"]
        self.model = InferenceModel(raw_response["model"])
        self.file = InferenceFile(raw_response["file"])


TypeBaseInference = TypeVar("TypeBaseInference", bound=BaseInference)
