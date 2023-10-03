from typing import Optional

from mindee.parsing.common.string_dict import StringDict
from mindee.parsing.standard.base import BaseField


class OrientationField(BaseField):
    """The clockwise rotation to apply (in degrees) to make the image upright."""

    value: int
    """Degrees as an integer."""

    def __init__(
        self,
        raw_prediction: StringDict,
        value_key: str = "value",
        reconstructed: bool = False,
        page_id: Optional[int] = None,
    ):
        """
        Page orientation.

        :param raw_prediction: Orientation prediction object from HTTP response
        :param value_key: Key to use in the orientation_prediction dict
        :param reconstructed: Bool for reconstructed object (not extracted in the API)
        :param page_id: Page number for multi-page document
        """
        super().__init__(
            raw_prediction,
            value_key=value_key,
            reconstructed=reconstructed,
            page_id=page_id,
        )

        try:
            self.value = int(raw_prediction[value_key])
            if self.value not in [0, 90, 180, 270]:
                self.value = 0
        except (TypeError, ValueError, KeyError):
            self.value = 0
