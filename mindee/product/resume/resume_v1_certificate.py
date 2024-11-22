from typing import Dict, Optional

from mindee.parsing.common.string_dict import StringDict
from mindee.parsing.common.summary_helper import clean_out_string, format_for_display
from mindee.parsing.standard.base import FieldConfidenceMixin, FieldPositionMixin


class ResumeV1Certificate(FieldPositionMixin, FieldConfidenceMixin):
    """The list of certificates obtained by the candidate."""

    grade: Optional[str]
    """The grade obtained for the certificate."""
    name: Optional[str]
    """The name of certification."""
    provider: Optional[str]
    """The organization or institution that issued the certificate."""
    year: Optional[str]
    """The year when a certificate was issued or received."""
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

        self.grade = raw_prediction["grade"]
        self.name = raw_prediction["name"]
        self.provider = raw_prediction["provider"]
        self.year = raw_prediction["year"]

    def _printable_values(self) -> Dict[str, str]:
        """Return values for printing."""
        out_dict: Dict[str, str] = {}
        out_dict["grade"] = format_for_display(self.grade)
        out_dict["name"] = format_for_display(self.name)
        out_dict["provider"] = format_for_display(self.provider)
        out_dict["year"] = format_for_display(self.year)
        return out_dict

    def _table_printable_values(self) -> Dict[str, str]:
        """Return values for printing inside an RST table."""
        out_dict: Dict[str, str] = {}
        out_dict["grade"] = format_for_display(self.grade, 10)
        out_dict["name"] = format_for_display(self.name, 30)
        out_dict["provider"] = format_for_display(self.provider, 25)
        out_dict["year"] = format_for_display(self.year, None)
        return out_dict

    def to_table_line(self) -> str:
        """Output in a format suitable for inclusion in an rST table."""
        printable = self._table_printable_values()
        out_str: str = f"| {printable['grade']:<10} | "
        out_str += f"{printable['name']:<30} | "
        out_str += f"{printable['provider']:<25} | "
        out_str += f"{printable['year']:<4} | "
        return clean_out_string(out_str)

    def __str__(self) -> str:
        """Default string representation."""
        printable = self._printable_values()
        out_str: str = f"Grade: {printable['grade']}, \n"
        out_str += f"Name: {printable['name']}, \n"
        out_str += f"Provider: {printable['provider']}, \n"
        out_str += f"Year: {printable['year']}, \n"
        return clean_out_string(out_str)
