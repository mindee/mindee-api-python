from typing import Dict, Optional

from mindee.parsing.common.string_dict import StringDict
from mindee.parsing.common.summary_helper import clean_out_string, format_for_display
from mindee.parsing.standard.base import FieldConfidenceMixin, FieldPositionMixin


class ResumeV1ProfessionalExperience(FieldPositionMixin, FieldConfidenceMixin):
    """The list of the candidate's professional experiences."""

    contract_type: Optional[str]
    """The type of contract for the professional experience."""
    department: Optional[str]
    """The specific department or division within the company."""
    description: Optional[str]
    """The description of the professional experience as written in the document."""
    employer: Optional[str]
    """The name of the company or organization."""
    end_month: Optional[str]
    """The month when the professional experience ended."""
    end_year: Optional[str]
    """The year when the professional experience ended."""
    role: Optional[str]
    """The position or job title held by the candidate."""
    start_month: Optional[str]
    """The month when the professional experience began."""
    start_year: Optional[str]
    """The year when the professional experience began."""
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

        self.contract_type = raw_prediction["contract_type"]
        self.department = raw_prediction["department"]
        self.description = raw_prediction["description"]
        self.employer = raw_prediction["employer"]
        self.end_month = raw_prediction["end_month"]
        self.end_year = raw_prediction["end_year"]
        self.role = raw_prediction["role"]
        self.start_month = raw_prediction["start_month"]
        self.start_year = raw_prediction["start_year"]

    def _printable_values(self) -> Dict[str, str]:
        """Return values for printing."""
        out_dict: Dict[str, str] = {}
        out_dict["contract_type"] = format_for_display(self.contract_type)
        out_dict["department"] = format_for_display(self.department)
        out_dict["description"] = format_for_display(self.description)
        out_dict["employer"] = format_for_display(self.employer)
        out_dict["end_month"] = format_for_display(self.end_month)
        out_dict["end_year"] = format_for_display(self.end_year)
        out_dict["role"] = format_for_display(self.role)
        out_dict["start_month"] = format_for_display(self.start_month)
        out_dict["start_year"] = format_for_display(self.start_year)
        return out_dict

    def _table_printable_values(self) -> Dict[str, str]:
        """Return values for printing inside an RST table."""
        out_dict: Dict[str, str] = {}
        out_dict["contract_type"] = format_for_display(self.contract_type, 15)
        out_dict["department"] = format_for_display(self.department, 10)
        out_dict["description"] = format_for_display(self.description, 36)
        out_dict["employer"] = format_for_display(self.employer, 25)
        out_dict["end_month"] = format_for_display(self.end_month, None)
        out_dict["end_year"] = format_for_display(self.end_year, None)
        out_dict["role"] = format_for_display(self.role, 20)
        out_dict["start_month"] = format_for_display(self.start_month, None)
        out_dict["start_year"] = format_for_display(self.start_year, None)
        return out_dict

    def to_table_line(self) -> str:
        """Output in a format suitable for inclusion in an rST table."""
        printable = self._table_printable_values()
        out_str: str = f"| {printable['contract_type']:<15} | "
        out_str += f"{printable['department']:<10} | "
        out_str += f"{printable['description']:<36} | "
        out_str += f"{printable['employer']:<25} | "
        out_str += f"{printable['end_month']:<9} | "
        out_str += f"{printable['end_year']:<8} | "
        out_str += f"{printable['role']:<20} | "
        out_str += f"{printable['start_month']:<11} | "
        out_str += f"{printable['start_year']:<10} | "
        return clean_out_string(out_str)

    def __str__(self) -> str:
        """Default string representation."""
        printable = self._printable_values()
        out_str: str = f"Contract Type: {printable['contract_type']}, \n"
        out_str += f"Department: {printable['department']}, \n"
        out_str += f"Description: {printable['description']}, \n"
        out_str += f"Employer: {printable['employer']}, \n"
        out_str += f"End Month: {printable['end_month']}, \n"
        out_str += f"End Year: {printable['end_year']}, \n"
        out_str += f"Role: {printable['role']}, \n"
        out_str += f"Start Month: {printable['start_month']}, \n"
        out_str += f"Start Year: {printable['start_year']}, \n"
        return clean_out_string(out_str)
