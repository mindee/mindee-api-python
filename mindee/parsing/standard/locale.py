from typing import Optional

from mindee.parsing.common.string_dict import StringDict
from mindee.parsing.standard.base import BaseField


class LocaleField(BaseField):
    """The locale detected on the document."""

    language: Optional[str]
    """The ISO 639-1 code of the language."""
    country: Optional[str]
    """The ISO 3166-1 alpha-2 code of the country."""
    currency: Optional[str]
    """The ISO 4217 code of the currency."""

    def __init__(
        self,
        raw_prediction: StringDict,
        reconstructed: bool = False,
        page_id: Optional[int] = None,
    ):
        """
        Locale field object.

        :param raw_prediction: Locale prediction object from HTTP response
        :param reconstructed: Bool for reconstructed object (not extracted in the API)
        :param page_id: Page number for multi-page document
        """
        value_key = (
            "value"
            if ("value" in raw_prediction and raw_prediction["value"])
            else "language"
        )

        super().__init__(
            raw_prediction,
            value_key=value_key,
            reconstructed=reconstructed,
            page_id=page_id,
        )
        self.language = self._get_value(raw_prediction, "language")
        self.country = self._get_value(raw_prediction, "country")
        self.currency = self._get_value(raw_prediction, "currency")

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
