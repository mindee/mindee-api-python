from typing import Optional

from mindee.parsing.standard.base import (
    BaseField,
    FieldPositionMixin,
    TypePredictionField,
)


class CompanyRegistrationField(FieldPositionMixin, BaseField):
    """A company registration item."""

    type: str
    """The type of registration."""

    def __init__(
        self,
        prediction: TypePredictionField,
        value_key: str = "value",
        reconstructed: bool = False,
        page_id: Optional[int] = None,
    ):
        super().__init__(prediction, value_key, reconstructed, page_id)
        self.type = prediction["type"]
        self._set_position(prediction)

    def __str__(self) -> str:
        if self.value:
            return f"{self.type}: {self.value}"
        return ""
