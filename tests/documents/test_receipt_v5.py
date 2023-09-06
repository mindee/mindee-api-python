import json

import pytest

from mindee.documents import ReceiptV5

RECEIPT_DATA_DIR = "./tests/data/products/expense_receipts"
FILE_PATH_RECEIPT_V5_COMPLETE = f"{ RECEIPT_DATA_DIR }/response_v5/complete.json"
FILE_PATH_RECEIPT_V5_EMPTY = f"{ RECEIPT_DATA_DIR }/response_v5/empty.json"


@pytest.fixture
def receipt_v5_doc() -> ReceiptV5:
    json_data = json.load(open(FILE_PATH_RECEIPT_V5_COMPLETE))
    return ReceiptV5(json_data["document"]["inference"], page_n=None)


@pytest.fixture
def receipt_v5_doc_empty() -> ReceiptV5:
    json_data = json.load(open(FILE_PATH_RECEIPT_V5_EMPTY))
    return ReceiptV5(json_data["document"]["inference"], page_n=None)


@pytest.fixture
def receipt_v5_page0():
    json_data = json.load(open(FILE_PATH_RECEIPT_V5_COMPLETE))
    return ReceiptV5(json_data["document"]["inference"]["pages"][0], page_n=0)


def test_empty_doc_constructor(receipt_v5_doc_empty):
    assert receipt_v5_doc_empty.locale.value is None
    assert receipt_v5_doc_empty.date.value is None
    assert receipt_v5_doc_empty.time.value is None
    assert receipt_v5_doc_empty.total_amount.value is None
    assert receipt_v5_doc_empty.total_net.value is None
    assert receipt_v5_doc_empty.total_tax.value is None
    assert receipt_v5_doc_empty.tip.value is None
    assert len(receipt_v5_doc_empty.taxes) == 0
    assert receipt_v5_doc_empty.supplier_name.value is None
    assert len(receipt_v5_doc_empty.supplier_company_registrations) == 0
    assert receipt_v5_doc_empty.supplier_address.value is None
    assert receipt_v5_doc_empty.supplier_phone_number.value is None
    assert len(receipt_v5_doc_empty.line_items) == 0


def test_doc_constructor(receipt_v5_doc):
    file_path = f"{ RECEIPT_DATA_DIR }/response_v5/doc_to_string.rst"
    reference_str = open(file_path, "r", encoding="utf-8").read()
    assert str(receipt_v5_doc) == reference_str


def test_page0_constructor(receipt_v5_page0):
    file_path = f"{ RECEIPT_DATA_DIR }/response_v5/page0_to_string.rst"
    reference_str = open(file_path, "r", encoding="utf-8").read()
    assert str(receipt_v5_page0) == reference_str
