import json

import pytest

from mindee.parsing.common.document import Document
from mindee.parsing.common.page import Page
from mindee.product.us import BankCheckV1
from mindee.product.us.bank_check.bank_check_v1_document import BankCheckV1Document
from mindee.product.us.bank_check.bank_check_v1_page import BankCheckV1Page
from tests.product import PRODUCT_DATA_DIR


@pytest.fixture
def complete_doc() -> Document[BankCheckV1Document, Page[BankCheckV1Page]]:
    json_data = json.load(
        open(
            PRODUCT_DATA_DIR / "bank_check" / "response_v1" / "complete.json",
            encoding="utf-8",
        )
    )
    return Document(BankCheckV1, json_data["document"])


@pytest.fixture
def empty_doc() -> Document[BankCheckV1Document, Page[BankCheckV1Page]]:
    json_data = json.load(
        open(
            PRODUCT_DATA_DIR / "bank_check" / "response_v1" / "empty.json",
            encoding="utf-8",
        )
    )
    return Document(BankCheckV1, json_data["document"])


@pytest.fixture
def complete_page_0() -> Page[BankCheckV1Page]:
    json_data = json.load(
        open(
            PRODUCT_DATA_DIR / "bank_check" / "response_v1" / "complete.json",
            encoding="utf-8",
        )
    )
    return Page(BankCheckV1Page, json_data["document"]["inference"]["pages"][0])


def test_complete_doc(
    complete_doc: Document[BankCheckV1Document, Page[BankCheckV1Page]]
):
    reference_str = open(
        PRODUCT_DATA_DIR / "bank_check" / "response_v1" / "summary_full.rst",
        "r",
        encoding="utf-8",
    ).read()
    assert str(complete_doc) == reference_str


def test_empty_doc(empty_doc: Document[BankCheckV1Document, Page[BankCheckV1Page]]):
    prediction = empty_doc.inference.prediction
    assert prediction.date.value is None
    assert prediction.amount.value is None
    assert len(prediction.payees) == 0
    assert prediction.routing_number.value is None
    assert prediction.account_number.value is None
    assert prediction.check_number.value is None


def test_complete_page_0(complete_page_0: Page[BankCheckV1Page]):
    reference_str = open(
        PRODUCT_DATA_DIR / "bank_check" / "response_v1" / "summary_page0.rst",
        "r",
        encoding="utf-8",
    ).read()
    assert complete_page_0.id == 0
    assert str(complete_page_0) == reference_str
