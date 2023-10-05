import json

import pytest

from mindee.parsing.common.document import Document
from mindee.parsing.common.page import Page
from mindee.product import ReceiptV4
from mindee.product.receipt.receipt_v4_document import ReceiptV4Document
from tests import RECEIPT_DATA_DIR

FILE_PATH_RECEIPT_V4_COMPLETE = f"{RECEIPT_DATA_DIR}/response_v4/complete.json"
FILE_PATH_RECEIPT_V4_EMPTY = f"{RECEIPT_DATA_DIR}/response_v4/empty.json"
FILE_PATH_SUMMARY_FULL = f"{RECEIPT_DATA_DIR}/response_v4/summary_full.rst"
FILE_PATH_PAGE_0 = f"{RECEIPT_DATA_DIR}/response_v4/summary_page0.rst"


@pytest.fixture
def complete_doc() -> Document[ReceiptV4Document, Page[ReceiptV4Document]]:
    json_data = json.load(open(FILE_PATH_RECEIPT_V4_COMPLETE))
    return Document(ReceiptV4, json_data["document"])


@pytest.fixture
def empty_doc() -> Document[ReceiptV4Document, Page[ReceiptV4Document]]:
    json_data = json.load(open(FILE_PATH_RECEIPT_V4_EMPTY))
    return Document(ReceiptV4, json_data["document"])


@pytest.fixture
def complete_page_0() -> Page[ReceiptV4Document]:
    json_data = json.load(open(FILE_PATH_RECEIPT_V4_COMPLETE))
    return Page(ReceiptV4Document, json_data["document"]["inference"]["pages"][0])


def test_complete_doc(
    complete_doc: Document[ReceiptV4Document, Page[ReceiptV4Document]]
):
    reference_str = open(FILE_PATH_SUMMARY_FULL, "r", encoding="utf-8").read()
    assert str(complete_doc) == reference_str


def test_empty_doc(empty_doc: Document[ReceiptV4Document, Page[ReceiptV4Document]]):
    prediction = empty_doc.inference.prediction
    assert prediction.locale.value is None
    assert prediction.date.value is None
    assert prediction.time.value is None
    assert prediction.total_amount.value is None
    assert prediction.total_net.value is None
    assert prediction.total_tax.value is None
    assert prediction.tip.value is None
    assert len(prediction.taxes) == 0
    assert prediction.supplier.value is None


def test_complete_page(complete_page_0: Page[ReceiptV4Document]):
    reference_str = open(FILE_PATH_PAGE_0, "r", encoding="utf-8").read()
    assert complete_page_0.orientation
    assert complete_page_0.orientation.value == 0
    assert complete_page_0.id == 0
    assert str(complete_page_0) == reference_str
