from typing import Optional

from mindee.fields.base import BaseField, TypePrediction


class LocaleField(BaseField):
    language: Optional[str] = None
    """Language ISO code"""
    country: Optional[str] = None
    """Country ISO code"""
    currency: Optional[str] = None
    """3 letter currency code"""

    def __init__(
        self,
        prediction: TypePrediction,
        value_key: str = "value",
        reconstructed: bool = False,
        page_n: Optional[int] = None,
    ):
        """
        Locale field object.

        :param prediction: Locale prediction object from HTTP response
        :param value_key: Key to use in the locale_prediction dict
        :param reconstructed: Bool for reconstructed object (not extracted in the API)
        :param page_n: Page number for multi-page document
        """
        super().__init__(
            prediction,
            value_key=value_key,
            reconstructed=reconstructed,
            page_n=page_n,
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
