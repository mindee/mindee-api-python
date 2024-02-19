from typing import Dict, Optional

from mindee.parsing.common import StringDict, clean_out_string, format_for_display
from mindee.parsing.standard import FieldConfidenceMixin, FieldPositionMixin


class ResumeV1ProfessionalExperience(FieldPositionMixin, FieldConfidenceMixin):
    """The list of values that represent the professional experiences of an individual in their global resume."""

    contract_type: Optional[str]
    """The type of contract for a professional experience. Possible values: 'Full-Time', 'Part-Time', 'Internship' and 'Freelance'."""
    department: Optional[str]
    """The specific department or division within a company where the professional experience was gained."""
    employer: Optional[str]
    """The name of the company or organization where the candidate has worked."""
    end_month: Optional[str]
    """The month when a professional experience ended."""
    end_year: Optional[str]
    """The year when a professional experience ended."""
    role: Optional[str]
    """The position or job title held by the individual in their previous work experience."""
    start_month: Optional[str]
    """The month when a professional experience began."""
    start_year: Optional[str]
    """The year when a professional experience began."""
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
        self.employer = raw_prediction["employer"]
        self.end_month = raw_prediction["end_month"]
        self.end_year = raw_prediction["end_year"]
        self.role = raw_prediction["role"]
        self.start_month = raw_prediction["start_month"]
        self.start_year = raw_prediction["start_year"]

    def _printable_values(self) -> Dict[str, str]:
        """Return values for printing."""
        out_dict: Dict[str, str] = {}
        out_dict["contract_type"] = format_for_display(self.contract_type, None)
        out_dict["department"] = format_for_display(self.department, None)
        out_dict["employer"] = format_for_display(self.employer, None)
        out_dict["end_month"] = format_for_display(self.end_month, None)
        out_dict["end_year"] = format_for_display(self.end_year, None)
        out_dict["role"] = format_for_display(self.role, None)
        out_dict["start_month"] = format_for_display(self.start_month, None)
        out_dict["start_year"] = format_for_display(self.start_year, None)
        return out_dict

    def to_table_line(self) -> str:
        """Output in a format suitable for inclusion in an rST table."""
        printable = self._printable_values()
        out_str: str = f"| {printable['contract_type']:<13} | "
        out_str += f"{printable['department']:<10} | "
        out_str += f"{printable['employer']:<8} | "
        out_str += f"{printable['end_month']:<9} | "
        out_str += f"{printable['end_year']:<8} | "
        out_str += f"{printable['role']:<4} | "
        out_str += f"{printable['start_month']:<11} | "
        out_str += f"{printable['start_year']:<10} | "
        return clean_out_string(out_str)

    def __str__(self) -> str:
        """Default string representation."""
        printable = self._printable_values()
        out_str: str = f"Contract Type: {printable['contract_type']}, \n"
        out_str += f"Department: {printable['department']}, \n"
        out_str += f"Employer: {printable['employer']}, \n"
        out_str += f"End Month: {printable['end_month']}, \n"
        out_str += f"End Year: {printable['end_year']}, \n"
        out_str += f"Role: {printable['role']}, \n"
        out_str += f"Start Month: {printable['start_month']}, \n"
        out_str += f"Start Year: {printable['start_year']}, \n"
        return clean_out_string(out_str)
