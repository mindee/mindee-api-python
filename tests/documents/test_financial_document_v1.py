import json

import pytest

from mindee.documents import FinancialDocumentV1

FINANCIAL_DOC_DATA_DIR = "./tests/data/products/financial_document"
FILE_PATH_FINANCIAL_DOC_V1_INVOICE = (
    f"{FINANCIAL_DOC_DATA_DIR}/response_v1/complete_invoice.json"
)
FILE_PATH_FINANCIAL_DOC_V1_RECEIPT = (
    f"{FINANCIAL_DOC_DATA_DIR}/response_v1/complete_receipt.json"
)
FILE_PATH_FINANCIAL_DOC_V1_EMPTY = f"{FINANCIAL_DOC_DATA_DIR}/response_v1/empty.json"


@pytest.fixture
def financial_doc_from_invoice_object():
    json_data = json.load(open(FILE_PATH_FINANCIAL_DOC_V1_INVOICE))
    return FinancialDocumentV1(
        api_prediction=json_data["document"]["inference"], page_n=None
    )


@pytest.fixture
def financial_doc_from_receipt_object():
    json_data = json.load(open(FILE_PATH_FINANCIAL_DOC_V1_RECEIPT))
    return FinancialDocumentV1(
        api_prediction=json_data["document"]["inference"], page_n=None
    )


@pytest.fixture
def financial_doc_object_all_na():
    json_data = json.load(open(FILE_PATH_FINANCIAL_DOC_V1_EMPTY))
    return FinancialDocumentV1(
        api_prediction=json_data["document"]["inference"]["pages"][0]
    )


def test_doc_constructor_invoice(financial_doc_from_invoice_object):
    assert financial_doc_from_invoice_object.date.value == "2019-02-11"
    assert (
        financial_doc_from_invoice_object.supplier_address.value
        == "4490 Oak Drive Albany, NY 12210"
    )
    doc_str = open(f"{FINANCIAL_DOC_DATA_DIR}/response_v1/invoice_to_string.rst").read()
    assert str(financial_doc_from_invoice_object) == doc_str


def test_doc_constructor_receipt(financial_doc_from_receipt_object):
    assert financial_doc_from_receipt_object.date.value == "2014-07-07"
    assert financial_doc_from_receipt_object.supplier_address.value is None
    doc_str = open(f"{FINANCIAL_DOC_DATA_DIR}/response_v1/receipt_to_string.rst").read()
    assert str(financial_doc_from_receipt_object) == doc_str


def test_all_na(financial_doc_object_all_na):
    assert financial_doc_object_all_na.orientation is None
    assert financial_doc_object_all_na.locale.value is None
    assert financial_doc_object_all_na.total_amount.value is None
    assert financial_doc_object_all_na.date.value is None
    assert financial_doc_object_all_na.supplier_name.value is None
    assert financial_doc_object_all_na.total_tax.value is None
    assert len(financial_doc_object_all_na.taxes) == 0
