from typing import List, Optional

from mindee.parsing.common.prediction import Prediction
from mindee.parsing.common.string_dict import StringDict
from mindee.parsing.common.summary_helper import clean_out_string
from mindee.product.fr.payslip.payslip_v3_bank_account_detail import (
    PayslipV3BankAccountDetail,
)
from mindee.product.fr.payslip.payslip_v3_employee import PayslipV3Employee
from mindee.product.fr.payslip.payslip_v3_employer import PayslipV3Employer
from mindee.product.fr.payslip.payslip_v3_employment import PayslipV3Employment
from mindee.product.fr.payslip.payslip_v3_paid_time_off import PayslipV3PaidTimeOff
from mindee.product.fr.payslip.payslip_v3_pay_detail import PayslipV3PayDetail
from mindee.product.fr.payslip.payslip_v3_pay_period import PayslipV3PayPeriod
from mindee.product.fr.payslip.payslip_v3_salary_detail import PayslipV3SalaryDetail


class PayslipV3Document(Prediction):
    """Payslip API version 3.0 document data."""

    bank_account_details: PayslipV3BankAccountDetail
    """Information about the employee's bank account."""
    employee: PayslipV3Employee
    """Information about the employee."""
    employer: PayslipV3Employer
    """Information about the employer."""
    employment: PayslipV3Employment
    """Information about the employment."""
    paid_time_off: List[PayslipV3PaidTimeOff]
    """Information about paid time off."""
    pay_detail: PayslipV3PayDetail
    """Detailed information about the pay."""
    pay_period: PayslipV3PayPeriod
    """Information about the pay period."""
    salary_details: List[PayslipV3SalaryDetail]
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
        self.bank_account_details = PayslipV3BankAccountDetail(
            raw_prediction["bank_account_details"],
            page_id=page_id,
        )
        self.employee = PayslipV3Employee(
            raw_prediction["employee"],
            page_id=page_id,
        )
        self.employer = PayslipV3Employer(
            raw_prediction["employer"],
            page_id=page_id,
        )
        self.employment = PayslipV3Employment(
            raw_prediction["employment"],
            page_id=page_id,
        )
        self.paid_time_off = [
            PayslipV3PaidTimeOff(prediction, page_id=page_id)
            for prediction in raw_prediction["paid_time_off"]
        ]
        self.pay_detail = PayslipV3PayDetail(
            raw_prediction["pay_detail"],
            page_id=page_id,
        )
        self.pay_period = PayslipV3PayPeriod(
            raw_prediction["pay_period"],
            page_id=page_id,
        )
        self.salary_details = [
            PayslipV3SalaryDetail(prediction, page_id=page_id)
            for prediction in raw_prediction["salary_details"]
        ]

    @staticmethod
    def _salary_details_separator(char: str) -> str:
        out_str = "  "
        out_str += f"+{char * 14}"
        out_str += f"+{char * 11}"
        out_str += f"+{char * 38}"
        out_str += f"+{char * 8}"
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
        out_str += " | Number"
        out_str += " | Rate     "
        out_str += f" |\n{self._salary_details_separator('=')}"
        out_str += f"\n  {lines}"
        out_str += f"\n{self._salary_details_separator('-')}"
        return out_str

    @staticmethod
    def _paid_time_off_separator(char: str) -> str:
        out_str = "  "
        out_str += f"+{char * 11}"
        out_str += f"+{char * 8}"
        out_str += f"+{char * 13}"
        out_str += f"+{char * 11}"
        out_str += f"+{char * 11}"
        return out_str + "+"

    def _paid_time_off_to_str(self) -> str:
        if not self.paid_time_off:
            return ""

        lines = f"\n{self._paid_time_off_separator('-')}\n  ".join(
            [item.to_table_line() for item in self.paid_time_off]
        )
        out_str = ""
        out_str += f"\n{self._paid_time_off_separator('-')}\n "
        out_str += " | Accrued  "
        out_str += " | Period"
        out_str += " | Type       "
        out_str += " | Remaining"
        out_str += " | Used     "
        out_str += f" |\n{self._paid_time_off_separator('=')}"
        out_str += f"\n  {lines}"
        out_str += f"\n{self._paid_time_off_separator('-')}"
        return out_str

    def __str__(self) -> str:
        out_str: str = f":Pay Period:\n{self.pay_period.to_field_list()}\n"
        out_str += f":Employee:\n{self.employee.to_field_list()}\n"
        out_str += f":Employer:\n{self.employer.to_field_list()}\n"
        out_str += (
            f":Bank Account Details:\n{self.bank_account_details.to_field_list()}\n"
        )
        out_str += f":Employment:\n{self.employment.to_field_list()}\n"
        out_str += f":Salary Details: {self._salary_details_to_str()}\n"
        out_str += f":Pay Detail:\n{self.pay_detail.to_field_list()}\n"
        out_str += f":Paid Time Off: {self._paid_time_off_to_str()}\n"
        return clean_out_string(out_str)
