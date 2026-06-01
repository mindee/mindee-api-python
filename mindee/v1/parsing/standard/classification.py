from typing import Optional

from mindee.parsing.common import StringDict
from mindee.v1.parsing.standard.base import BaseField


class ClassificationField(BaseField):
    """Represents a classifier value."""

    value: str
    """The value as a string."""

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
        super().__init__(
            raw_prediction,
            value_key=value_key,
            reconstructed=reconstructed,
            page_id=page_id,
        )
