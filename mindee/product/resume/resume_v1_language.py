from typing import Dict, Optional

from mindee.parsing.common.string_dict import StringDict
from mindee.parsing.common.summary_helper import clean_out_string, format_for_display
from mindee.parsing.standard.base import FieldConfidenceMixin, FieldPositionMixin


class ResumeV1Language(FieldPositionMixin, FieldConfidenceMixin):
    """The list of languages that the candidate is proficient in."""

    language: Optional[str]
    """The language's ISO 639 code."""
    level: Optional[str]
    """The candidate's level for the language."""
    page_n: int
    """The document page on which the information was found."""

    def __init__(
        self,
        raw_prediction: StringDict,
        page_id: Optional[int] = None,
    ):
        self._set_confidence(raw_prediction)
        self._set_position(raw_prediction)

        if page_id is None:
            try:
                self.page_n = raw_prediction["page_id"]
            except KeyError:
                pass
        else:
            self.page_n = page_id

        self.language = raw_prediction["language"]
        self.level = raw_prediction["level"]

    def _printable_values(self) -> Dict[str, str]:
        """Return values for printing."""
        out_dict: Dict[str, str] = {}
        out_dict["language"] = format_for_display(self.language)
        out_dict["level"] = format_for_display(self.level)
        return out_dict

    def _table_printable_values(self) -> Dict[str, str]:
        """Return values for printing inside an RST table."""
        out_dict: Dict[str, str] = {}
        out_dict["language"] = format_for_display(self.language, None)
        out_dict["level"] = format_for_display(self.level, 20)
        return out_dict

    def to_table_line(self) -> str:
        """Output in a format suitable for inclusion in an rST table."""
        printable = self._table_printable_values()
        out_str: str = f"| {printable['language']:<8} | "
        out_str += f"{printable['level']:<20} | "
        return clean_out_string(out_str)

    def __str__(self) -> str:
        """Default string representation."""
        printable = self._printable_values()
        out_str: str = f"Language: {printable['language']}, \n"
        out_str += f"Level: {printable['level']}, \n"
        return clean_out_string(out_str)
