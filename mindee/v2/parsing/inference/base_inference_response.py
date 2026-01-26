from typing import TypeVar, Generic

from mindee.parsing.common.string_dict import StringDict
from mindee.v2.parsing.inference.base_inference import TypeBaseInference

from mindee.parsing.v2.common_response import CommonResponse


class BaseInferenceResponse(CommonResponse, Generic[TypeBaseInference]):
    """Base class for V2 inference responses."""

    inference: TypeBaseInference
    """The inference result for a split utility request"""

    def __init__(self, raw_response: StringDict) -> None:
        super().__init__(raw_response)
        self.inference = self._set_inference_type(raw_response["inference"])

    def _set_inference_type(self, inference_response: StringDict):
        """
        Sets the inference type.

        :param inference_response: Server response.
        """
        raise NotImplementedError()


TypeInferenceResponse = TypeVar("TypeInferenceResponse", bound=BaseInferenceResponse)
