from typing import Dict, Optional

from mindee.parsing.common.string_dict import StringDict
from mindee.parsing.common.summary_helper import clean_out_string, format_for_display
from mindee.parsing.standard.base import FieldConfidenceMixin, FieldPositionMixin


class PayslipV3Employment(FieldPositionMixin, FieldConfidenceMixin):
    """Information about the employment."""

    category: Optional[str]
    """The category of the employment."""
    coefficient: Optional[str]
    """The coefficient of the employment."""
    collective_agreement: Optional[str]
    """The collective agreement of the employment."""
    job_title: Optional[str]
    """The job title of the employee."""
    position_level: Optional[str]
    """The position level of the employment."""
    seniority_date: Optional[str]
    """The seniority date of the employment."""
    start_date: Optional[str]
    """The start date of the employment."""
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

        self.category = raw_prediction["category"]
        self.coefficient = raw_prediction["coefficient"]
        self.collective_agreement = raw_prediction["collective_agreement"]
        self.job_title = raw_prediction["job_title"]
        self.position_level = raw_prediction["position_level"]
        self.seniority_date = raw_prediction["seniority_date"]
        self.start_date = raw_prediction["start_date"]

    def _printable_values(self) -> Dict[str, str]:
        """Return values for printing."""
        out_dict: Dict[str, str] = {}
        out_dict["category"] = format_for_display(self.category)
        out_dict["coefficient"] = format_for_display(self.coefficient)
        out_dict["collective_agreement"] = format_for_display(self.collective_agreement)
        out_dict["job_title"] = format_for_display(self.job_title)
        out_dict["position_level"] = format_for_display(self.position_level)
        out_dict["seniority_date"] = format_for_display(self.seniority_date)
        out_dict["start_date"] = format_for_display(self.start_date)
        return out_dict

    def to_field_list(self) -> str:
        """Output the object in a format suitable for inclusion in an rST field list."""
        printable = self._printable_values()
        out_str: str = f"  :Category: {printable['category']}\n"
        out_str += f"  :Coefficient: {printable['coefficient']}\n"
        out_str += f"  :Collective Agreement: {printable['collective_agreement']}\n"
        out_str += f"  :Job Title: {printable['job_title']}\n"
        out_str += f"  :Position Level: {printable['position_level']}\n"
        out_str += f"  :Seniority Date: {printable['seniority_date']}\n"
        out_str += f"  :Start Date: {printable['start_date']}\n"
        return out_str.rstrip()

    def __str__(self) -> str:
        """Default string representation."""
        printable = self._printable_values()
        out_str: str = f"Category: {printable['category']}, \n"
        out_str += f"Coefficient: {printable['coefficient']}, \n"
        out_str += f"Collective Agreement: {printable['collective_agreement']}, \n"
        out_str += f"Job Title: {printable['job_title']}, \n"
        out_str += f"Position Level: {printable['position_level']}, \n"
        out_str += f"Seniority Date: {printable['seniority_date']}, \n"
        out_str += f"Start Date: {printable['start_date']}, \n"
        return clean_out_string(out_str)
