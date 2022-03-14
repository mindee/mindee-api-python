from typing import Optional

from mindee.fields.base import Field


class Amount(Field):
    value: Optional[float] = None

    def __init__(
        self,
        amount_prediction: dict,
        value_key: str = "amount",
        reconstructed: bool = False,
        page_n=None,
    ):
        """
        Amount field object.

        :param amount_prediction: Amount prediction object from HTTP response
        :param value_key: Key to use in the amount_prediction dict
        :param reconstructed: Bool for reconstructed object (not extracted in the API)
        :param page_n: Page number for multi pages pdf
        """
        super().__init__(
            amount_prediction,
            value_key=value_key,
            reconstructed=reconstructed,
            page_n=page_n,
        )

        try:
            self.value = round(float(amount_prediction[value_key]), 3)
        except (ValueError, TypeError, KeyError):
            self.value = None
            self.confidence = 0.0
