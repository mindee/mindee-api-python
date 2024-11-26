import json

import pytest

from mindee.parsing.common.document import Document
from mindee.parsing.common.page import Page
from mindee.product.fr.payslip.payslip_v3 import PayslipV3
from mindee.product.fr.payslip.payslip_v3_document import (
    PayslipV3Document,
)
from tests.product import PRODUCT_DATA_DIR

RESPONSE_DIR = PRODUCT_DATA_DIR / "payslip_fra" / "response_v3"

PayslipV3DocumentType = Document[
    PayslipV3Document,
    Page[PayslipV3Document],
]


@pytest.fixture
def complete_doc() -> PayslipV3DocumentType:
    file_path = RESPONSE_DIR / "complete.json"
    with open(file_path, "r", encoding="utf-8") as open_file:
        json_data = json.load(open_file)
    return Document(PayslipV3, json_data["document"])


@pytest.fixture
def empty_doc() -> PayslipV3DocumentType:
    file_path = RESPONSE_DIR / "empty.json"
    with open(file_path, "r", encoding="utf-8") as open_file:
        json_data = json.load(open_file)
    return Document(PayslipV3, json_data["document"])


def test_complete_doc(complete_doc: PayslipV3DocumentType):
    file_path = RESPONSE_DIR / "summary_full.rst"
    with open(file_path, "r", encoding="utf-8") as open_file:
        reference_str = open_file.read()
    assert str(complete_doc) == reference_str


def test_empty_doc(empty_doc: PayslipV3DocumentType):
    prediction = empty_doc.inference.prediction
    assert prediction.pay_period.end_date is None
    assert prediction.pay_period.month is None
    assert prediction.pay_period.payment_date is None
    assert prediction.pay_period.start_date is None
    assert prediction.pay_period.year is None
    assert prediction.employee.address is None
    assert prediction.employee.date_of_birth is None
    assert prediction.employee.first_name is None
    assert prediction.employee.last_name is None
    assert prediction.employee.phone_number is None
    assert prediction.employee.registration_number is None
    assert prediction.employee.social_security_number is None
    assert prediction.employer.address is None
    assert prediction.employer.company_id is None
    assert prediction.employer.company_site is None
    assert prediction.employer.naf_code is None
    assert prediction.employer.name is None
    assert prediction.employer.phone_number is None
    assert prediction.employer.urssaf_number is None
    assert prediction.bank_account_details.bank_name is None
    assert prediction.bank_account_details.iban is None
    assert prediction.bank_account_details.swift is None
    assert prediction.employment.category is None
    assert prediction.employment.coefficient is None
    assert prediction.employment.collective_agreement is None
    assert prediction.employment.job_title is None
    assert prediction.employment.position_level is None
    assert prediction.employment.seniority_date is None
    assert prediction.employment.start_date is None
    assert len(prediction.salary_details) == 0
    assert prediction.pay_detail.gross_salary is None
    assert prediction.pay_detail.gross_salary_ytd is None
    assert prediction.pay_detail.income_tax_rate is None
    assert prediction.pay_detail.income_tax_withheld is None
    assert prediction.pay_detail.net_paid is None
    assert prediction.pay_detail.net_paid_before_tax is None
    assert prediction.pay_detail.net_taxable is None
    assert prediction.pay_detail.net_taxable_ytd is None
    assert prediction.pay_detail.total_cost_employer is None
    assert prediction.pay_detail.total_taxes_and_deductions is None
    assert len(prediction.paid_time_off) == 0
