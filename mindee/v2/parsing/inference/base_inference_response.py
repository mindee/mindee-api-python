from typing import ClassVar, Type, TypeVar, Generic

from mindee.parsing.common.string_dict import StringDict
from mindee.v2.parsing.inference.base_inference import BaseInference, TypeBaseInference

from mindee.parsing.v2.common_response import CommonResponse


class BaseInferenceResponse(CommonResponse, Generic[TypeBaseInference]):
    """Base class for V2 inference responses."""

    inference: BaseInference
    """The inference result for a split utility request"""
    inference_type: ClassVar[Type[BaseInference]]
    """Inference class used for slug derivation."""

    def __init__(self, raw_response: StringDict) -> None:
        super().__init__(raw_response)
        self.inference = self._set_inference_type(raw_response["inference"])

    def _set_inference_type(self, inference_response: StringDict):
        """
        Sets the inference type.

        :param inference_response: Server response.
        """
        raise NotImplementedError()

    @classmethod
    def get_inference_slug(cls) -> str:
        """Getter for the inference slug."""
        return cls.inference_type.get_slug()


TypeInferenceResponse = TypeVar("TypeInferenceResponse", bound=BaseInferenceResponse)
