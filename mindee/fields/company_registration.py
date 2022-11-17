from typing import Optional

from mindee.fields.base import BaseField, FieldPositionMixin, TypePrediction


class CompanyRegistrationField(FieldPositionMixin, BaseField):
    type: str
    """The type of registration."""

    def __init__(
        self,
        prediction: TypePrediction,
        value_key: str = "value",
        reconstructed: bool = False,
        page_n: Optional[int] = None,
    ):
        super().__init__(prediction, value_key, reconstructed, page_n)
        self.type = prediction["type"]
        self._set_position(prediction)

    def __str__(self) -> str:
        if self.value:
            return f"{self.type}: {self.value}"
        return ""
