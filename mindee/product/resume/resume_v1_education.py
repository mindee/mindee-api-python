from typing import Dict, Optional

from mindee.parsing.common.string_dict import StringDict
from mindee.parsing.common.summary_helper import clean_out_string, format_for_display
from mindee.parsing.standard.base import FieldConfidenceMixin, FieldPositionMixin


class ResumeV1Education(FieldPositionMixin, FieldConfidenceMixin):
    """The list of the candidate's educational background."""

    degree_domain: Optional[str]
    """The area of study or specialization."""
    degree_type: Optional[str]
    """The type of degree obtained, such as Bachelor's, Master's, or Doctorate."""
    end_month: Optional[str]
    """The month when the education program or course was completed."""
    end_year: Optional[str]
    """The year when the education program or course was completed."""
    school: Optional[str]
    """The name of the school."""
    start_month: Optional[str]
    """The month when the education program or course began."""
    start_year: Optional[str]
    """The year when the education program or course began."""
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

        self.degree_domain = raw_prediction["degree_domain"]
        self.degree_type = raw_prediction["degree_type"]
        self.end_month = raw_prediction["end_month"]
        self.end_year = raw_prediction["end_year"]
        self.school = raw_prediction["school"]
        self.start_month = raw_prediction["start_month"]
        self.start_year = raw_prediction["start_year"]

    def _printable_values(self) -> Dict[str, str]:
        """Return values for printing."""
        out_dict: Dict[str, str] = {}
        out_dict["degree_domain"] = format_for_display(self.degree_domain)
        out_dict["degree_type"] = format_for_display(self.degree_type)
        out_dict["end_month"] = format_for_display(self.end_month)
        out_dict["end_year"] = format_for_display(self.end_year)
        out_dict["school"] = format_for_display(self.school)
        out_dict["start_month"] = format_for_display(self.start_month)
        out_dict["start_year"] = format_for_display(self.start_year)
        return out_dict

    def _table_printable_values(self) -> Dict[str, str]:
        """Return values for printing inside an RST table."""
        out_dict: Dict[str, str] = {}
        out_dict["degree_domain"] = format_for_display(self.degree_domain, 15)
        out_dict["degree_type"] = format_for_display(self.degree_type, 25)
        out_dict["end_month"] = format_for_display(self.end_month, None)
        out_dict["end_year"] = format_for_display(self.end_year, None)
        out_dict["school"] = format_for_display(self.school, 25)
        out_dict["start_month"] = format_for_display(self.start_month, None)
        out_dict["start_year"] = format_for_display(self.start_year, None)
        return out_dict

    def to_table_line(self) -> str:
        """Output in a format suitable for inclusion in an rST table."""
        printable = self._table_printable_values()
        out_str: str = f"| {printable['degree_domain']:<15} | "
        out_str += f"{printable['degree_type']:<25} | "
        out_str += f"{printable['end_month']:<9} | "
        out_str += f"{printable['end_year']:<8} | "
        out_str += f"{printable['school']:<25} | "
        out_str += f"{printable['start_month']:<11} | "
        out_str += f"{printable['start_year']:<10} | "
        return clean_out_string(out_str)

    def __str__(self) -> str:
        """Default string representation."""
        printable = self._printable_values()
        out_str: str = f"Domain: {printable['degree_domain']}, \n"
        out_str += f"Degree: {printable['degree_type']}, \n"
        out_str += f"End Month: {printable['end_month']}, \n"
        out_str += f"End Year: {printable['end_year']}, \n"
        out_str += f"School: {printable['school']}, \n"
        out_str += f"Start Month: {printable['start_month']}, \n"
        out_str += f"Start Year: {printable['start_year']}, \n"
        return clean_out_string(out_str)
