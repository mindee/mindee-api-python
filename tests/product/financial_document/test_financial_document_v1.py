import json

import pytest

from mindee.parsing.common.document import Document
from mindee.parsing.common.page import Page
from mindee.product import FinancialDocumentV1
from mindee.product.financial_document.financial_document_v1_document import (
    FinancialDocumentV1Document,
)
from tests.product import PRODUCT_DATA_DIR


@pytest.fixture
def complete_doc_invoice() -> (
    Document[FinancialDocumentV1Document, Page[FinancialDocumentV1Document]]
):
    json_data = json.load(
        open(
            PRODUCT_DATA_DIR
            / "financial_document"
            / "response_v1"
            / "complete_invoice.json"
        )
    )
    return Document(FinancialDocumentV1, json_data["document"])


@pytest.fixture
def complete_doc_receipt() -> (
    Document[FinancialDocumentV1Document, Page[FinancialDocumentV1Document]]
):
    json_data = json.load(
        open(
            PRODUCT_DATA_DIR
            / "financial_document"
            / "response_v1"
            / "complete_receipt.json"
        )
    )
    return Document(FinancialDocumentV1, json_data["document"])


@pytest.fixture
def empty_doc() -> (
    Document[FinancialDocumentV1Document, Page[FinancialDocumentV1Document]]
):
    json_data = json.load(
        open(PRODUCT_DATA_DIR / "financial_document" / "response_v1" / "empty.json")
    )
    return Document(FinancialDocumentV1, json_data["document"])


@pytest.fixture
def complete_page_0_invoice() -> Page[FinancialDocumentV1Document]:
    json_data = json.load(
        open(
            PRODUCT_DATA_DIR
            / "financial_document"
            / "response_v1"
            / "complete_invoice.json"
        )
    )
    return Page(
        FinancialDocumentV1Document, json_data["document"]["inference"]["pages"][0]
    )


@pytest.fixture
def complete_page_0_receipt() -> Page[FinancialDocumentV1Document]:
    json_data = json.load(
        open(
            PRODUCT_DATA_DIR
            / "financial_document"
            / "response_v1"
            / "complete_receipt.json"
        )
    )
    return Page(
        FinancialDocumentV1Document, json_data["document"]["inference"]["pages"][0]
    )


# def test_complete_doc(
#     complete_doc_invoice: Document[
#         FinancialDocumentV1Document, Page[FinancialDocumentV1Document]
#     ],
#     complete_doc_receipt: Document[
#         FinancialDocumentV1Document, Page[FinancialDocumentV1Document]
#     ],
# ):
#     reference_str_invoice = open(
#         PRODUCT_DATA_DIR
#         / "financial_document"
#         / "response_v1"
#         / "summary_full_invoice.rst",
#         "r",
#         encoding="utf-8",
#     ).read()
#     reference_str_receipt = open(
#         PRODUCT_DATA_DIR
#         / "financial_document"
#         / "response_v1"
#         / "summary_full_receipt.rst",
#         "r",
#         encoding="utf-8",
#     ).read()
#     assert str(complete_doc_invoice) == reference_str_invoice
#     assert str(complete_doc_receipt) == reference_str_receipt


def test_empty_doc(
    empty_doc: Document[FinancialDocumentV1Document, Page[FinancialDocumentV1Document]]
):
    prediction = empty_doc.inference.prediction
    assert prediction.locale.value is None
    assert prediction.invoice_number.value is None
    assert len(prediction.reference_numbers) == 0
    assert prediction.date.value is None
    assert prediction.due_date.value is None
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


# def test_complete_page_0(
#     complete_page_0_invoice: Page[FinancialDocumentV1Document],
#     complete_page_0_receipt: Page[FinancialDocumentV1Document],
# ):
#     reference_str_invoice = open(
#         PRODUCT_DATA_DIR
#         / "financial_document"
#         / "response_v1"
#         / "summary_page0_invoice.rst",
#         "r",
#         encoding="utf-8",
#     ).read()
#     reference_str_receipt = open(
#         PRODUCT_DATA_DIR
#         / "financial_document"
#         / "response_v1"
#         / "summary_page0_receipt.rst",
#         "r",
#         encoding="utf-8",
#     ).read()
#     assert complete_page_0_invoice.id == 0
#     assert complete_page_0_receipt.id == 0
#     assert str(complete_page_0_invoice) == reference_str_invoice
#     assert str(complete_page_0_receipt) == reference_str_receipt
