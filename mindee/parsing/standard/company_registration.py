from typing import Optional

from mindee.parsing.common.string_dict import StringDict
from mindee.parsing.standard.base import BaseField, FieldPositionMixin


class CompanyRegistrationField(FieldPositionMixin, BaseField):
    """A company registration item."""

    type: str
    """The type of registration."""

    def __init__(
        self,
        raw_prediction: StringDict,
        value_key: str = "value",
        reconstructed: bool = False,
        page_id: Optional[int] = None,
    ):
        super().__init__(raw_prediction, value_key, reconstructed, page_id)
        self.type = raw_prediction["type"]
        self._set_position(raw_prediction)

    def print(self) -> str:
        """Additional print function that doesn't overwrite __str__()."""
        if self.value:
            return f"{self.type}: {self.value}"
        return ""
