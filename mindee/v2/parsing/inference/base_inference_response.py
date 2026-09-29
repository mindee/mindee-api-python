from abc import ABC
from typing import ClassVar, TypeVar

from mindee.parsing.common.common_response import CommonResponse
from mindee.v2.parsing.inference.base_inference import BaseInference


class BaseInferenceResponse(ABC, CommonResponse):
    """Base class for V2 inference responses."""

    inference: BaseInference
    """The inference result for a split utility request"""

    _slug: ClassVar[str]
    """Slug of the product."""

    def __str__(self) -> str:
        return str(self.inference)

    @classmethod
    def get_product_slug(cls) -> str:
        """Get the product's slug."""
        return cls._slug


TypeBaseInferenceResponse = TypeVar(
    "TypeBaseInferenceResponse", bound=BaseInferenceResponse
)
