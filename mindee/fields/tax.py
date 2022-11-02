from typing import Optional

from mindee.fields.base import BaseField, FieldPositionMixin, TypePrediction


class TaxField(FieldPositionMixin, BaseField):
    value: Optional[float]
    """The amount of the tax line."""
    rate: Optional[float]
    """The tax rate, represented as a float between 0 and 1."""
    code: Optional[str]
    "The tax code."
    basis: Optional[float]
    "The amount used to calculate the tax."

    def __init__(
        self,
        prediction: TypePrediction,
        value_key: str = "value",
        rate_key: str = "rate",
        code_key: str = "code",
        reconstructed: bool = False,
        page_n: Optional[int] = None,
    ):
        """
        Tax field object.

        :param prediction: Tax prediction object from HTTP response
        :param value_key: Key to use in the tax_prediction dict
        :param rate_key: Key to use for getting the Tax rate in the tax_prediction dict
        :param code_key: Key to use for getting the Tax code in the tax_prediction dict
        :param reconstructed: Bool for reconstructed object (not extracted in the API)
        :param page_n: Page number for multi pages document
        """
        super().__init__(
            prediction,
            value_key=value_key,
            reconstructed=reconstructed,
            page_n=page_n,
        )

        self._set_position(prediction)

        try:
            self.rate = float(prediction[rate_key])
        except (ValueError, TypeError, KeyError):
            self.rate = None

        try:
            self.code = str(prediction[code_key])
        except (TypeError, KeyError):
            self.code = None
        if self.code in ("N/A", "None"):
            self.code = None

        try:
            self.basis = float(prediction["basis"])
        except (ValueError, TypeError, KeyError):
            self.basis = None

        try:
            self.value = float(prediction[value_key])
        except (ValueError, TypeError, KeyError):
            self.value = None
            self.confidence = 0.0

    def __str__(self) -> str:
        out_str = ""
        if self.value is not None:
            out_str += str(self.value)
        if self.rate is not None:
            out_str += f" {self.rate}%"
        if self.code is not None:
            out_str += f" {self.code}"
        return out_str.strip()
