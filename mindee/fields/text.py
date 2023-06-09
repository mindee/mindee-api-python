from typing import Optional

from mindee.fields.base import BaseField, FieldPositionMixin, TypePrediction


class TextField(FieldPositionMixin, BaseField):
    """A field containing a text value."""

    value: Optional[str] = None

    def __init__(
        self,
        prediction: TypePrediction,
        value_key: str = "value",
        reconstructed: bool = False,
        page_id: Optional[int] = None,
    ):
        """
        Text field object.

        :param prediction: Amount prediction object from HTTP response
        :param value_key: Key to use in the amount_prediction dict
        :param reconstructed: Bool for reconstructed object (not extracted in the API)
        :param page_id: Page number for multi-page document
        """
        super().__init__(
            prediction,
            value_key=value_key,
            reconstructed=reconstructed,
            page_n=page_id,
        )
        self._set_position(prediction)
