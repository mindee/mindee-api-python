from typing import Optional

from mindee.fields.base import BaseField, TypePrediction


class OrientationField(BaseField):
    """The clockwise rotation to apply (in degrees) to make the image upright."""

    value: int
    """Degrees as an integer."""

    def __init__(
        self,
        prediction: TypePrediction,
        value_key: str = "value",
        reconstructed: bool = False,
        page_n: Optional[int] = None,
    ):
        """
        Page orientation.

        :param prediction: Orientation prediction object from HTTP response
        :param value_key: Key to use in the orientation_prediction dict
        :param reconstructed: Bool for reconstructed object (not extracted in the API)
        :param page_n: Page number for multi-page document
        """
        super().__init__(
            prediction,
            value_key=value_key,
            reconstructed=reconstructed,
            page_n=page_n,
        )

        try:
            self.value = int(prediction[value_key])
            if self.value not in [0, 90, 180, 270]:
                self.value = 0
        except (TypeError, ValueError, KeyError):
            self.value = 0
