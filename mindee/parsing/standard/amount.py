from typing import Optional

from mindee.parsing.common.string_dict import StringDict
from mindee.parsing.standard.base import BaseField, FieldPositionMixin, float_to_string


class AmountField(FieldPositionMixin, BaseField):
    """A field containing an amount value."""

    value: Optional[float]
    """The amount value as a float."""

    def __init__(
        self,
        raw_prediction: StringDict,
        reconstructed: bool = False,
        page_id: Optional[int] = None,
    ):
        """
        Amount field object.

        :param raw_prediction: Amount prediction object from HTTP response
        :param reconstructed: Bool for reconstructed object (not extracted in the API)
        :param page_id: Page number for multi-page document
        """
        self.value = None
        super().__init__(
            raw_prediction,
            value_key="value",
            reconstructed=reconstructed,
            page_id=page_id,
        )
        try:
            self.value = round(float(raw_prediction["value"]), 3)
        except (ValueError, TypeError, KeyError):
            self.value = None
            self.confidence = 0.0

        self._set_position(raw_prediction)

    def __str__(self) -> str:
        return float_to_string(self.value)
