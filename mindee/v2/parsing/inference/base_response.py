from abc import ABC

from mindee.v2.parsing.inference.base_inference import BaseInference

from mindee.parsing.v2.common_response import CommonResponse


class BaseResponse(ABC, CommonResponse):
    """Base class for V2 inference responses."""

    inference: BaseInference
    """The inference result for a split utility request"""
    _slug: str
    """Slug of the inference."""

    def __str__(self) -> str:
        return str(self.inference)

    @classmethod
    def get_result_slug(cls) -> str:
        """Getter for the inference slug."""
        return cls._slug
