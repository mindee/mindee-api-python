from typing import Dict, Optional

from mindee.parsing.common.string_dict import StringDict
from mindee.parsing.common.summary_helper import clean_out_string
from mindee.parsing.standard.base import (
    FieldConfidenceMixin,
    FieldPositionMixin,
    float_to_string,
    to_opt_float,
)


class PayslipV3PayDetail(FieldPositionMixin, FieldConfidenceMixin):
    """Detailed information about the pay."""

    gross_salary: Optional[float]
    """The gross salary of the employee."""
    gross_salary_ytd: Optional[float]
    """The year-to-date gross salary of the employee."""
    income_tax_rate: Optional[float]
    """The income tax rate of the employee."""
    income_tax_withheld: Optional[float]
    """The income tax withheld from the employee's pay."""
    net_paid: Optional[float]
    """The net paid amount of the employee."""
    net_paid_before_tax: Optional[float]
    """The net paid amount before tax of the employee."""
    net_taxable: Optional[float]
    """The net taxable amount of the employee."""
    net_taxable_ytd: Optional[float]
    """The year-to-date net taxable amount of the employee."""
    total_cost_employer: Optional[float]
    """The total cost to the employer."""
    total_taxes_and_deductions: Optional[float]
    """The total taxes and deductions of the employee."""
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

        self.gross_salary = to_opt_float(raw_prediction, "gross_salary")
        self.gross_salary_ytd = to_opt_float(raw_prediction, "gross_salary_ytd")
        self.income_tax_rate = to_opt_float(raw_prediction, "income_tax_rate")
        self.income_tax_withheld = to_opt_float(raw_prediction, "income_tax_withheld")
        self.net_paid = to_opt_float(raw_prediction, "net_paid")
        self.net_paid_before_tax = to_opt_float(raw_prediction, "net_paid_before_tax")
        self.net_taxable = to_opt_float(raw_prediction, "net_taxable")
        self.net_taxable_ytd = to_opt_float(raw_prediction, "net_taxable_ytd")
        self.total_cost_employer = to_opt_float(raw_prediction, "total_cost_employer")
        self.total_taxes_and_deductions = to_opt_float(
            raw_prediction, "total_taxes_and_deductions"
        )

    def _printable_values(self) -> Dict[str, str]:
        """Return values for printing."""
        out_dict: Dict[str, str] = {}
        out_dict["gross_salary"] = float_to_string(self.gross_salary)
        out_dict["gross_salary_ytd"] = float_to_string(self.gross_salary_ytd)
        out_dict["income_tax_rate"] = float_to_string(self.income_tax_rate)
        out_dict["income_tax_withheld"] = float_to_string(self.income_tax_withheld)
        out_dict["net_paid"] = float_to_string(self.net_paid)
        out_dict["net_paid_before_tax"] = float_to_string(self.net_paid_before_tax)
        out_dict["net_taxable"] = float_to_string(self.net_taxable)
        out_dict["net_taxable_ytd"] = float_to_string(self.net_taxable_ytd)
        out_dict["total_cost_employer"] = float_to_string(self.total_cost_employer)
        out_dict["total_taxes_and_deductions"] = float_to_string(
            self.total_taxes_and_deductions
        )
        return out_dict

    def to_field_list(self) -> str:
        """Output the object in a format suitable for inclusion in an rST field list."""
        printable = self._printable_values()
        out_str: str = f"  :Gross Salary: {printable['gross_salary']}\n"
        out_str += f"  :Gross Salary YTD: {printable['gross_salary_ytd']}\n"
        out_str += f"  :Income Tax Rate: {printable['income_tax_rate']}\n"
        out_str += f"  :Income Tax Withheld: {printable['income_tax_withheld']}\n"
        out_str += f"  :Net Paid: {printable['net_paid']}\n"
        out_str += f"  :Net Paid Before Tax: {printable['net_paid_before_tax']}\n"
        out_str += f"  :Net Taxable: {printable['net_taxable']}\n"
        out_str += f"  :Net Taxable YTD: {printable['net_taxable_ytd']}\n"
        out_str += f"  :Total Cost Employer: {printable['total_cost_employer']}\n"
        out_str += f"  :Total Taxes and Deductions: {printable['total_taxes_and_deductions']}\n"
        return out_str.rstrip()

    def __str__(self) -> str:
        """Default string representation."""
        printable = self._printable_values()
        out_str: str = f"Gross Salary: {printable['gross_salary']}, \n"
        out_str += f"Gross Salary YTD: {printable['gross_salary_ytd']}, \n"
        out_str += f"Income Tax Rate: {printable['income_tax_rate']}, \n"
        out_str += f"Income Tax Withheld: {printable['income_tax_withheld']}, \n"
        out_str += f"Net Paid: {printable['net_paid']}, \n"
        out_str += f"Net Paid Before Tax: {printable['net_paid_before_tax']}, \n"
        out_str += f"Net Taxable: {printable['net_taxable']}, \n"
        out_str += f"Net Taxable YTD: {printable['net_taxable_ytd']}, \n"
        out_str += f"Total Cost Employer: {printable['total_cost_employer']}, \n"
        out_str += (
            f"Total Taxes and Deductions: {printable['total_taxes_and_deductions']}, \n"
        )
        return clean_out_string(out_str)
