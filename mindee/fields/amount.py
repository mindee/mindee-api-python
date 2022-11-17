from typing import Optional

from mindee.fields.base import BaseField, FieldPositionMixin, TypePrediction


class AmountField(FieldPositionMixin, BaseField):
    value: Optional[float] = None

    def __init__(
        self,
        prediction: TypePrediction,
        reconstructed: bool = False,
        page_n: Optional[int] = None,
    ):
        """
        Amount field object.

        :param prediction: Amount prediction object from HTTP response
        :param reconstructed: Bool for reconstructed object (not extracted in the API)
        :param page_n: Page number for multi-page document
        """
        super().__init__(
            prediction,
            value_key="value",
            reconstructed=reconstructed,
            page_n=page_n,
        )
        try:
            self.value = round(float(prediction["value"]), 3)
        except (ValueError, TypeError, KeyError):
            self.value = None
            self.confidence = 0.0

        self._set_position(prediction)
