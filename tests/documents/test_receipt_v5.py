import json

import pytest

from mindee.documents import ReceiptV5
from tests import RECEIPT_DATA_DIR

FILE_PATH_RECEIPT_V5_COMPLETE = f"{RECEIPT_DATA_DIR}/response_v5/complete.json"
FILE_PATH_RECEIPT_V5_EMPTY = f"{RECEIPT_DATA_DIR}/response_v5/empty.json"


@pytest.fixture
def receipt_v5_doc_object():
    json_data = json.load(open(FILE_PATH_RECEIPT_V5_COMPLETE))
    return ReceiptV5(api_prediction=json_data["document"]["inference"], page_n=None)


@pytest.fixture
def receipt_v5_doc_object_empty():
    json_data = json.load(open(FILE_PATH_RECEIPT_V5_EMPTY))
    return ReceiptV5(api_prediction=json_data["document"]["inference"], page_n=None)


@pytest.fixture
def receipt_v5_page_object():
    json_data = json.load(open(FILE_PATH_RECEIPT_V5_COMPLETE))
    return ReceiptV5(
        api_prediction=json_data["document"]["inference"]["pages"][0], page_n=0
    )


def test_doc_constructor(receipt_v5_doc_object: ReceiptV5):
    assert receipt_v5_doc_object.date.value == "2016-02-26"
    assert receipt_v5_doc_object.total_tax.value == 1.7
    doc_str = open(f"{RECEIPT_DATA_DIR}/response_v5/doc_to_string.rst").read()
    assert receipt_v5_doc_object.orientation is None
    assert receipt_v5_doc_object.date.page_n == 0
    assert str(receipt_v5_doc_object) == doc_str
    assert receipt_v5_doc_object.taxes[0].basis == 8.5


def test_page_constructor(receipt_v5_page_object: ReceiptV5):
    assert receipt_v5_page_object.date.value == "2016-02-26"
    assert receipt_v5_page_object.total_tax.value == 1.7
    doc_str = open(f"{RECEIPT_DATA_DIR}/response_v5/page0_to_string.rst").read()
    assert receipt_v5_page_object.orientation.value == 0
    assert receipt_v5_page_object.date.page_n == 0
    assert str(receipt_v5_page_object) == doc_str
    assert len(receipt_v5_page_object.cropper) == 0
    assert receipt_v5_page_object.taxes[0].basis == 8.5


def test_all_na(receipt_v5_doc_object_empty: ReceiptV5):
    assert receipt_v5_doc_object_empty.locale.value is None
    assert receipt_v5_doc_object_empty.total_amount.value is None
    assert receipt_v5_doc_object_empty.date.value is None
    assert receipt_v5_doc_object_empty.supplier_name.value is None
    assert receipt_v5_doc_object_empty.time.value is None
    assert receipt_v5_doc_object_empty.orientation is None
    assert receipt_v5_doc_object_empty.total_tax.value is None
    assert len(receipt_v5_doc_object_empty.taxes) == 0


def test_checklist_on_empty(receipt_v5_doc_object_empty):
    for check in receipt_v5_doc_object_empty.checklist.values():
        assert check is False
