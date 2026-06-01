from typing import Optional

from mindee.parsing.common import StringDict
from mindee.v1.parsing.standard.base import BaseField, FieldPositionMixin


class StringField(FieldPositionMixin, BaseField):
    """A field containing a text value."""

    value: Optional[str]
    """Value of the string."""
    raw_value: Optional[str]
    """The value as it appears on the document."""

    def __init__(
        self,
        raw_prediction: StringDict,
        value_key: str = "value",
        reconstructed: bool = False,
        page_id: Optional[int] = None,
    ):
        """
        Text field object.

        :params raw_prediction: Amount prediction object from HTTP response
        :params value_key: Key to use in the amount_prediction dict
        :params reconstructed: Bool for reconstructed object (not extracted in the API)
        :params page_id: Page number for multi-page document
        """
        self.value = None
        super().__init__(
            raw_prediction,
            value_key=value_key,
            reconstructed=reconstructed,
            page_id=page_id,
        )
        self._set_position(raw_prediction)
        self.raw_value = raw_prediction.get("raw_value", None)
