import json

import pytest

from mindee.documents.receipt.receipt_v4 import ReceiptV4
from tests import RECEIPT_DATA_DIR

FILE_PATH_RECEIPT_V4_COMPLETE = f"{RECEIPT_DATA_DIR}/response_v4/complete.json"
FILE_PATH_RECEIPT_V4_EMPTY = f"{RECEIPT_DATA_DIR}/response_v4/empty.json"


@pytest.fixture
def receipt_v4_doc_object():
    json_data = json.load(open(FILE_PATH_RECEIPT_V4_COMPLETE))
    return ReceiptV4(api_prediction=json_data["document"]["inference"], page_n=None)


@pytest.fixture
def receipt_v4_doc_object_empty():
    json_data = json.load(open(FILE_PATH_RECEIPT_V4_EMPTY))
    return ReceiptV4(api_prediction=json_data["document"]["inference"], page_n=None)


@pytest.fixture
def receipt_v4_page_object():
    json_data = json.load(open(FILE_PATH_RECEIPT_V4_COMPLETE))
    return ReceiptV4(
        api_prediction=json_data["document"]["inference"]["pages"][0], page_n=0
    )


def test_doc_constructor(receipt_v4_doc_object):
    assert receipt_v4_doc_object.date.value == "2014-07-07"
    assert receipt_v4_doc_object.total_tax.value == 3.34
    doc_str = open(f"{RECEIPT_DATA_DIR}/response_v4/doc_to_string.txt").read().strip()
    assert receipt_v4_doc_object.orientation is None
    assert receipt_v4_doc_object.date.page_n == 0
    assert str(receipt_v4_doc_object) == doc_str


def test_page_constructor(receipt_v4_page_object):
    assert receipt_v4_page_object.date.value == "2014-07-07"
    assert receipt_v4_page_object.total_tax.value == 3.34
    doc_str = open(f"{RECEIPT_DATA_DIR}/response_v4/page0_to_string.txt").read().strip()
    assert receipt_v4_page_object.orientation.value == 0
    assert receipt_v4_page_object.date.page_n == 0
    assert str(receipt_v4_page_object) == doc_str
    assert len(receipt_v4_page_object.cropper) == 0


def test_cropper():
    json_data = json.load(
        open(f"{RECEIPT_DATA_DIR}/response_v4/complete_with_cropper.json")
    )
    receipt_v4_page_object = ReceiptV4(
        api_prediction=json_data["document"]["inference"]["pages"][0], page_n=0
    )
    assert len(receipt_v4_page_object.cropper) == 1
    assert len(receipt_v4_page_object.cropper[0].polygon) == 24


def test_all_na(receipt_v4_doc_object_empty):
    assert receipt_v4_doc_object_empty.locale.value is None
    assert receipt_v4_doc_object_empty.total_amount.value is None
    assert receipt_v4_doc_object_empty.date.value is None
    assert receipt_v4_doc_object_empty.supplier.value is None
    assert receipt_v4_doc_object_empty.time.value is None
    assert receipt_v4_doc_object_empty.orientation is None
    assert receipt_v4_doc_object_empty.total_tax.value is None
    assert len(receipt_v4_doc_object_empty.taxes) == 0


def test_checklist_on_empty(receipt_v4_doc_object_empty):
    for check in receipt_v4_doc_object_empty.checklist.values():
        assert check is False
