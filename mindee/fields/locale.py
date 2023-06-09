from typing import Optional

from mindee.fields.base import BaseField, TypePrediction


class LocaleField(BaseField):
    """The locale detected on the document."""

    language: Optional[str] = None
    """The ISO 639-1 code of the language."""
    country: Optional[str] = None
    """The ISO 3166-1 alpha-2 code of the country."""
    currency: Optional[str] = None
    """The ISO 4217 code of the currency."""

    def __init__(
        self,
        prediction: TypePrediction,
        reconstructed: bool = False,
        page_id: Optional[int] = None,
    ):
        """
        Locale field object.

        :param prediction: Locale prediction object from HTTP response
        :param reconstructed: Bool for reconstructed object (not extracted in the API)
        :param page_id: Page number for multi-page document
        """
        value_key = "value" if "value" in prediction else "language"

        super().__init__(
            prediction,
            value_key=value_key,
            reconstructed=reconstructed,
            page_n=page_id,
        )
        self.language = self._get_value(prediction, "language")
        self.country = self._get_value(prediction, "country")
        self.currency = self._get_value(prediction, "currency")

    @staticmethod
    def _get_value(locale_prediction: dict, key: str) -> Optional[str]:
        if key not in locale_prediction or locale_prediction[key] == "N/A":
            return None
        return locale_prediction[key]

    def __str__(self) -> str:
        out_str = ""
        if self.value is not None:
            out_str += self.value + "; "
        if self.language is not None:
            out_str += self.language + "; "
        if self.country is not None:
            out_str += self.country + "; "
        if self.currency is not None:
            out_str += self.currency + "; "
        return out_str.strip()
