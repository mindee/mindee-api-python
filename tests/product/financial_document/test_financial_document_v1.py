import json

import pytest

from mindee.parsing.common.document import Document
from mindee.parsing.common.page import Page
from mindee.product.financial_document.financial_document_v1 import FinancialDocumentV1
from mindee.product.financial_document.financial_document_v1_document import (
    FinancialDocumentV1Document,
)
from tests.product import PRODUCT_DATA_DIR

RESPONSE_DIR = PRODUCT_DATA_DIR / "financial_document" / "response_v1"

FinancialDocumentV1DocumentType = Document[
    FinancialDocumentV1Document,
    Page[FinancialDocumentV1Document],
]


@pytest.fixture
def complete_doc_invoice() -> FinancialDocumentV1DocumentType:
    file_path = RESPONSE_DIR / "complete_invoice.json"
    with open(file_path, "r", encoding="utf-8") as open_file:
        json_data = json.load(open_file)
    return Document(FinancialDocumentV1, json_data["document"])


@pytest.fixture
def complete_doc_receipt() -> FinancialDocumentV1DocumentType:
    file_path = RESPONSE_DIR / "complete_receipt.json"
    with open(file_path, "r", encoding="utf-8") as open_file:
        json_data = json.load(open_file)
    return Document(FinancialDocumentV1, json_data["document"])


@pytest.fixture
def empty_doc() -> FinancialDocumentV1DocumentType:
    file_path = RESPONSE_DIR / "empty.json"
    with open(file_path, "r", encoding="utf-8") as open_file:
        json_data = json.load(open_file)
    return Document(FinancialDocumentV1, json_data["document"])


@pytest.fixture
def complete_page0_invoice() -> Page[FinancialDocumentV1Document]:
    file_path = RESPONSE_DIR / "complete_invoice.json"
    with open(file_path, "r", encoding="utf-8") as open_file:
        json_data = json.load(open_file)
    page_0 = json_data["document"]["inference"]["pages"][0]
    return Page(FinancialDocumentV1Document, page_0)


@pytest.fixture
def complete_page0_receipt() -> Page[FinancialDocumentV1Document]:
    file_path = RESPONSE_DIR / "complete_receipt.json"
    with open(file_path, "r", encoding="utf-8") as open_file:
        json_data = json.load(open_file)
    page_0 = json_data["document"]["inference"]["pages"][0]
    return Page(FinancialDocumentV1Document, page_0)


def test_complete_invoice(complete_doc_invoice: FinancialDocumentV1DocumentType):
    file_path = RESPONSE_DIR / "summary_full_invoice.rst"
    with open(file_path, "r", encoding="utf-8") as open_file:
        reference_str = open_file.read()
    assert str(complete_doc_invoice) == reference_str


def test_complete_receipt(
    complete_doc_receipt: FinancialDocumentV1DocumentType,
):
    file_path = RESPONSE_DIR / "summary_full_receipt.rst"
    with open(file_path, "r", encoding="utf-8") as open_file:
        reference_str = open_file.read()
    assert str(complete_doc_receipt) == reference_str


def test_empty_doc(empty_doc: FinancialDocumentV1DocumentType):
    prediction = empty_doc.inference.prediction
    assert prediction.locale.value is None
    assert prediction.invoice_number.value is None
    assert len(prediction.reference_numbers) == 0
    assert prediction.billing_address.value is None
    assert len(prediction.customer_company_registrations) == 0
    assert prediction.customer_id.value is None
    assert prediction.customer_name.value is None
    assert prediction.date.value is None
    assert prediction.due_date.value is None
    assert prediction.document_type.value is not None
    assert prediction.document_type_extended.value is not None
    assert prediction.document_number.value is None
    assert prediction.total_net.value is None
    assert prediction.total_amount.value is None
    assert len(prediction.taxes) == 0
    assert len(prediction.supplier_payment_details) == 0
    assert prediction.supplier_name.value is None
    assert len(prediction.supplier_company_registrations) == 0
    assert prediction.supplier_address.value is None
    assert prediction.customer_name.value is None
    assert len(prediction.customer_company_registrations) == 0
    assert prediction.customer_address.value is None
    assert len(prediction.line_items) == 0


def test_page0_invoice(complete_page0_invoice: Page[FinancialDocumentV1Document]):
    file_path = RESPONSE_DIR / "summary_page0_invoice.rst"
    with open(file_path, "r", encoding="utf-8") as open_file:
        reference_str = open_file.read()
    assert complete_page0_invoice.id == 0
    assert str(complete_page0_invoice) == reference_str


def test_page0_receipt(complete_page0_receipt: Page[FinancialDocumentV1Document]):
    file_path = RESPONSE_DIR / "summary_page0_receipt.rst"
    with open(file_path, "r", encoding="utf-8") as open_file:
        reference_str = open_file.read()
    assert complete_page0_receipt.id == 0
    assert str(complete_page0_receipt) == reference_str
