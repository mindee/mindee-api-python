from typing import List, Optional

from mindee.parsing.common.prediction import Prediction
from mindee.parsing.common.string_dict import StringDict
from mindee.parsing.common.summary_helper import clean_out_string
from mindee.product.fr.payslip.payslip_v2_bank_account_detail import (
    PayslipV2BankAccountDetail,
)
from mindee.product.fr.payslip.payslip_v2_employee import PayslipV2Employee
from mindee.product.fr.payslip.payslip_v2_employer import PayslipV2Employer
from mindee.product.fr.payslip.payslip_v2_employment import PayslipV2Employment
from mindee.product.fr.payslip.payslip_v2_pay_detail import PayslipV2PayDetail
from mindee.product.fr.payslip.payslip_v2_pay_period import PayslipV2PayPeriod
from mindee.product.fr.payslip.payslip_v2_pto import PayslipV2Pto
from mindee.product.fr.payslip.payslip_v2_salary_detail import PayslipV2SalaryDetail


class PayslipV2Document(Prediction):
    """Payslip API version 2.0 document data."""

    bank_account_details: PayslipV2BankAccountDetail
    """Information about the employee's bank account."""
    employee: PayslipV2Employee
    """Information about the employee."""
    employer: PayslipV2Employer
    """Information about the employer."""
    employment: PayslipV2Employment
    """Information about the employment."""
    pay_detail: PayslipV2PayDetail
    """Detailed information about the pay."""
    pay_period: PayslipV2PayPeriod
    """Information about the pay period."""
    pto: PayslipV2Pto
    """Information about paid time off."""
    salary_details: List[PayslipV2SalaryDetail]
    """Detailed information about the earnings."""

    def __init__(
        self,
        raw_prediction: StringDict,
        page_id: Optional[int] = None,
    ):
        """
        Payslip document.

        :param raw_prediction: Raw prediction from HTTP response
        :param page_id: Page number for multi pages pdf input
        """
        super().__init__(raw_prediction, page_id)
        self.bank_account_details = PayslipV2BankAccountDetail(
            raw_prediction["bank_account_details"],
            page_id=page_id,
        )
        self.employee = PayslipV2Employee(
            raw_prediction["employee"],
            page_id=page_id,
        )
        self.employer = PayslipV2Employer(
            raw_prediction["employer"],
            page_id=page_id,
        )
        self.employment = PayslipV2Employment(
            raw_prediction["employment"],
            page_id=page_id,
        )
        self.pay_detail = PayslipV2PayDetail(
            raw_prediction["pay_detail"],
            page_id=page_id,
        )
        self.pay_period = PayslipV2PayPeriod(
            raw_prediction["pay_period"],
            page_id=page_id,
        )
        self.pto = PayslipV2Pto(
            raw_prediction["pto"],
            page_id=page_id,
        )
        self.salary_details = [
            PayslipV2SalaryDetail(prediction, page_id=page_id)
            for prediction in raw_prediction["salary_details"]
        ]

    @staticmethod
    def _salary_details_separator(char: str) -> str:
        out_str = "  "
        out_str += f"+{char * 14}"
        out_str += f"+{char * 11}"
        out_str += f"+{char * 38}"
        out_str += f"+{char * 11}"
        return out_str + "+"

    def _salary_details_to_str(self) -> str:
        if not self.salary_details:
            return ""

        lines = f"\n{self._salary_details_separator('-')}\n  ".join(
            [item.to_table_line() for item in self.salary_details]
        )
        out_str = ""
        out_str += f"\n{self._salary_details_separator('-')}\n "
        out_str += " | Amount      "
        out_str += " | Base     "
        out_str += " | Description                         "
        out_str += " | Rate     "
        out_str += f" |\n{self._salary_details_separator('=')}"
        out_str += f"\n  {lines}"
        out_str += f"\n{self._salary_details_separator('-')}"
        return out_str

    def __str__(self) -> str:
        out_str: str = f":Employee:\n{self.employee.to_field_list()}\n"
        out_str += f":Employer:\n{self.employer.to_field_list()}\n"
        out_str += (
            f":Bank Account Details:\n{self.bank_account_details.to_field_list()}\n"
        )
        out_str += f":Employment:\n{self.employment.to_field_list()}\n"
        out_str += f":Salary Details: {self._salary_details_to_str()}\n"
        out_str += f":Pay Detail:\n{self.pay_detail.to_field_list()}\n"
        out_str += f":PTO:\n{self.pto.to_field_list()}\n"
        out_str += f":Pay Period:\n{self.pay_period.to_field_list()}\n"
        return clean_out_string(out_str)
