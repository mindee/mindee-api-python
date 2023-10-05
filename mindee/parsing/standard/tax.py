from typing import Dict, List, Optional

from mindee.parsing.common.string_dict import StringDict
from mindee.parsing.standard.base import BaseField, FieldPositionMixin, float_to_string


class TaxField(FieldPositionMixin, BaseField):
    """Tax line information."""

    value: Optional[float]
    """The amount of the tax line."""
    rate: Optional[float]
    """The tax rate."""
    code: Optional[str]
    "The tax code (HST, GST... for Canadian; City Tax, State tax for US, etc..)."
    basis: Optional[float]
    "The tax base."

    def __init__(
        self,
        raw_prediction: StringDict,
        value_key: str = "value",
        reconstructed: bool = False,
        page_id: Optional[int] = None,
    ):
        """
        Tax field object.

        :param raw_prediction: Tax prediction object from HTTP response
        :param value_key: Key to use in the tax_prediction dict
        :param reconstructed: Bool for reconstructed object (not extracted in the API)
        :param page_id: Page number for multi pages document
        """
        super().__init__(
            raw_prediction,
            value_key=value_key,
            reconstructed=reconstructed,
            page_id=page_id,
        )

        self._set_position(raw_prediction)

        try:
            self.rate = float(raw_prediction["rate"])
        except (ValueError, TypeError, KeyError):
            self.rate = None

        try:
            self.code = str(raw_prediction["code"])
        except (TypeError, KeyError):
            self.code = None
        if self.code in ("N/A", "None"):
            self.code = None

        try:
            self.basis = float(raw_prediction["base"])
        except (ValueError, TypeError, KeyError):
            self.basis = None

        try:
            self.value = float(raw_prediction["value"])
        except (ValueError, TypeError, KeyError):
            self.value = None
            self.confidence = 0.0

    def _printable_values(self) -> Dict[str, str]:
        """Return values for printing."""
        return {
            "code": self.code if self.code is not None else "",
            "basis": float_to_string(self.basis),
            "rate": float_to_string(self.rate),
            "value": float_to_string(self.value),
        }

    def to_table_line(self) -> str:
        """Output in a format suitable for inclusion in an rST table."""
        printable = self._printable_values()
        return (
            f"| {printable['basis']:<13}"
            f" | {printable['code']:<6}"
            f" | {printable['rate']:<8}"
            f" | {printable['value']:<13}"
            " |"
        )

    def __str__(self) -> str:
        """Default string representation."""
        printable = self._printable_values()
        return (
            f"Base: {printable['basis']}, "
            f"Code: {printable['code']}, "
            f"Rate (%): {printable['rate']}, "
            f"Amount: {printable['value']}"
        ).strip()


class Taxes(List[TaxField]):
    """List of tax lines information."""

    @staticmethod
    def _line_separator(char: str):
        out_str = "  "
        out_str += f"+{char * 15}"
        out_str += f"+{char * 8}"
        out_str += f"+{char * 10}"
        out_str += f"+{char * 15}"
        return out_str + "+"

    def __init__(
        self, api_prediction: List[StringDict], page_id: Optional[int]
    ) -> None:
        super().__init__()
        for entry in api_prediction:
            tax = TaxField(entry, page_id=page_id)
            self.append(tax)

    def __str__(self) -> str:
        out_str = f"\n{self._line_separator('-')}\n"
        out_str += "  | Base          | Code   | Rate (%) | Amount        |\n"
        out_str += f"{self._line_separator('=')}"
        out_str += "\n".join(
            f"\n  {t.to_table_line()}\n{self._line_separator('-')}" for t in self
        )
        return out_str
