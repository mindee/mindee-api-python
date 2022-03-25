from mindee.fields.base import Field


class Orientation(Field):
    value: int
    """Orientation degrees. One of 0, 90, 180, 270"""

    def __init__(
        self,
        orientation_prediction: dict,
        value_key: str = "degrees",
        reconstructed: bool = False,
        page_n=None,
    ):
        """
        Page orientation.

        :param orientation_prediction: Orientation prediction object from HTTP response
        :param value_key: Key to use in the orientation_prediction dict
        :param reconstructed: Bool for reconstructed object (not extracted in the API)
        :param page_n: Page number for multi pages pdf
        """
        super().__init__(
            orientation_prediction,
            value_key=value_key,
            reconstructed=reconstructed,
            page_n=page_n,
        )

        try:
            self.value = int(orientation_prediction[value_key])
            if self.value not in [0, 90, 180, 270]:
                self.value = 0
        except (TypeError, ValueError, KeyError):
            self.value = 0
            self.confidence = 0.0
            self.bbox = []
