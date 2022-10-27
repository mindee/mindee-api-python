import json

import pytest

from mindee.documents.receipt.receipt_v4 import ReceiptV4
from tests import RECEIPT_DATA_DIR

RECEIPT_V4_FILE_PATH = f"{RECEIPT_DATA_DIR}/response_v4/complete.json"
RECEIPT_V4_NA_FILE_PATH = f"{RECEIPT_DATA_DIR}/response_v4/empty.json"


@pytest.fixture
def doc_object():
    json_data = json.load(open(RECEIPT_V4_FILE_PATH))
    return ReceiptV4(json_data["document"]["inference"]["prediction"], page_n=None)


@pytest.fixture
def doc_object_all_na():
    json_data = json.load(open(RECEIPT_V4_NA_FILE_PATH))
    return ReceiptV4(json_data["document"]["inference"]["prediction"], page_n=None)


@pytest.fixture
def page_object():
    json_data = json.load(open(RECEIPT_V4_FILE_PATH))
    return ReceiptV4(
        json_data["document"]["inference"]["pages"][0]["prediction"], page_n=0
    )


def test_doc_constructor(doc_object):
    assert doc_object.date.value == "2014-07-07"
    assert doc_object.total_tax.value == 3.34
    doc_str = open(f"{RECEIPT_DATA_DIR}/response_v4/doc_to_string.txt").read().strip()
    assert str(doc_object) == doc_str


def test_page_constructor(page_object):
    assert page_object.date.value == "2014-07-07"
    assert page_object.total_tax.value == 3.34
    doc_str = open(f"{RECEIPT_DATA_DIR}/response_v4/page0_to_string.txt").read().strip()
    assert str(page_object) == doc_str


def test_all_na(doc_object_all_na):
    assert doc_object_all_na.locale.value is None
    assert doc_object_all_na.total_amount.value is None
    assert doc_object_all_na.date.value is None
    assert doc_object_all_na.supplier.value is None
    assert doc_object_all_na.time.value is None
    assert doc_object_all_na.orientation is None
    assert doc_object_all_na.total_tax.value is None
    assert len(doc_object_all_na.taxes) == 0


def test_checklist_on_empty(doc_object_all_na):
    for check in doc_object_all_na.checklist.values():
        assert check is False
