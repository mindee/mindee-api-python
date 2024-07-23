from typing import Optional

from mindee.parsing.common.string_dict import StringDict
from mindee.parsing.standard.base import BaseField, FieldPositionMixin


class BooleanField(FieldPositionMixin, BaseField):
    """A field containing a boolean value."""

    value: Optional[bool]
    """The value as it appears on the document."""

    def __init__(
        self,
        raw_prediction: StringDict,
        value_key: str = "value",
        reconstructed: bool = False,
        page_id: Optional[int] = None,
    ):
        """
        Boolean field object.

        :param raw_prediction: Amount prediction object from HTTP response
        :param value_key: Key to use in the amount_prediction dict
        :param reconstructed: Bool for reconstructed object (not extracted in the API)
        :param page_id: Page number for multi-page document
        """
        self.value = None
        super().__init__(
            raw_prediction,
            value_key=value_key,
            reconstructed=reconstructed,
            page_id=page_id,
        )
        self._set_position(raw_prediction)
