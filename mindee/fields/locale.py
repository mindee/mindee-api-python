from typing import Optional
from mindee.fields.base import Field


class Locale(Field):
    language: Optional[str] = None
    country: Optional[str] = None
    currency: Optional[str] = None

    def __init__(
        self, locale_prediction, value_key="value", reconstructed=False, page_n=None
    ):
        """
        :param locale_prediction: Locale prediction object from HTTP response
        :param value_key: Key to use in the locale_prediction dict
        :param reconstructed: Bool for reconstructed object (not extracted in the API)
        :param page_n: Page number for multi pages pdf
        """
        super().__init__(
            locale_prediction,
            value_key=value_key,
            reconstructed=reconstructed,
            page_n=page_n,
        )
        self.language = self._get_value(locale_prediction, "language")
        self.country = self._get_value(locale_prediction, "country")
        self.currency = self._get_value(locale_prediction, "currency")

    @staticmethod
    def _get_value(locale_prediction, key: str):
        if (
            key not in locale_prediction.keys()
            or locale_prediction["language"] == "N/A"
        ):
            return None
        return locale_prediction[key]

    def __str__(self) -> str:
        output_str = f"{self.value}; "
        if self.language is not None:
            output_str += self.language + "; "
        if self.country is not None:
            output_str += self.country + "; "
        if self.currency is not None:
            output_str += self.currency + "; "
        return output_str.strip()
