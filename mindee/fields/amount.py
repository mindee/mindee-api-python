from typing import Optional

from mindee.fields.base import (
    BaseField,
    FieldPositionMixin,
    TypePrediction,
    float_to_string,
)


class AmountField(FieldPositionMixin, BaseField):
    """A field containing an amount value."""

    value: Optional[float] = None
    """The amount value as a float."""

    def __init__(
        self,
        prediction: TypePrediction,
        reconstructed: bool = False,
        page_id: Optional[int] = None,
    ):
        """
        Amount field object.

        :param prediction: Amount prediction object from HTTP response
        :param reconstructed: Bool for reconstructed object (not extracted in the API)
        :param page_id: Page number for multi-page document
        """
        super().__init__(
            prediction,
            value_key="value",
            reconstructed=reconstructed,
            page_n=page_id,
        )
        try:
            self.value = round(float(prediction["value"]), 3)
        except (ValueError, TypeError, KeyError):
            self.value = None
            self.confidence = 0.0

        self._set_position(prediction)

    def __str__(self) -> str:
        return float_to_string(self.value)
