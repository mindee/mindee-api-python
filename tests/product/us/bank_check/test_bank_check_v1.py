import json

import pytest

from mindee.parsing.common.document import Document
from mindee.parsing.common.page import Page
from mindee.product.us.bank_check.bank_check_v1 import BankCheckV1
from mindee.product.us.bank_check.bank_check_v1_document import (
    BankCheckV1Document,
)
from mindee.product.us.bank_check.bank_check_v1_page import (
    BankCheckV1Page,
)
from tests.product import PRODUCT_DATA_DIR

RESPONSE_DIR = PRODUCT_DATA_DIR / "bank_check" / "response_v1"

BankCheckV1DocumentType = Document[
    BankCheckV1Document,
    Page[BankCheckV1Page],
]


@pytest.fixture
def complete_doc() -> BankCheckV1DocumentType:
    file_path = RESPONSE_DIR / "complete.json"
    with open(file_path, "r", encoding="utf-8") as open_file:
        json_data = json.load(open_file)
    return Document(BankCheckV1, json_data["document"])


@pytest.fixture
def empty_doc() -> BankCheckV1DocumentType:
    file_path = RESPONSE_DIR / "empty.json"
    with open(file_path, "r", encoding="utf-8") as open_file:
        json_data = json.load(open_file)
    return Document(BankCheckV1, json_data["document"])


@pytest.fixture
def complete_page0() -> Page[BankCheckV1Page]:
    file_path = RESPONSE_DIR / "complete.json"
    with open(file_path, "r", encoding="utf-8") as open_file:
        json_data = json.load(open_file)
    page0 = json_data["document"]["inference"]["pages"][0]
    return Page(BankCheckV1Page, page0)


def test_complete_doc(complete_doc: BankCheckV1DocumentType):
    file_path = RESPONSE_DIR / "summary_full.rst"
    with open(file_path, "r", encoding="utf-8") as open_file:
        reference_str = open_file.read()
    assert str(complete_doc) == reference_str


def test_empty_doc(empty_doc: BankCheckV1DocumentType):
    prediction = empty_doc.inference.prediction
    assert prediction.date.value is None
    assert prediction.amount.value is None
    assert len(prediction.payees) == 0
    assert prediction.routing_number.value is None
    assert prediction.account_number.value is None
    assert prediction.check_number.value is None


def test_complete_page0(complete_page0: Page[BankCheckV1Page]):
    file_path = RESPONSE_DIR / "summary_page0.rst"
    with open(file_path, "r", encoding="utf-8") as open_file:
        reference_str = open_file.read()
    assert complete_page0.id == 0
    assert str(complete_page0) == reference_str
