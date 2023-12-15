import json

import pytest

from mindee.parsing.common.document import Document
from mindee.parsing.common.page import Page
from mindee.product.fr import BankAccountDetailsV1
from mindee.product.fr.bank_account_details.bank_account_details_v1_document import (
    BankAccountDetailsV1Document,
)
from tests.product import PRODUCT_DATA_DIR


@pytest.fixture
def complete_doc() -> (
    Document[BankAccountDetailsV1Document, Page[BankAccountDetailsV1Document]]
):
    json_data = json.load(
        open(
            PRODUCT_DATA_DIR / "bank_account_details" / "response_v1" / "complete.json",
            encoding="utf-8",
        )
    )
    return Document(BankAccountDetailsV1, json_data["document"])


@pytest.fixture
def empty_doc() -> (
    Document[BankAccountDetailsV1Document, Page[BankAccountDetailsV1Document]]
):
    json_data = json.load(
        open(
            PRODUCT_DATA_DIR / "bank_account_details" / "response_v1" / "empty.json",
            encoding="utf-8",
        )
    )
    return Document(BankAccountDetailsV1, json_data["document"])


@pytest.fixture
def complete_page_0() -> Page[BankAccountDetailsV1Document]:
    json_data = json.load(
        open(
            PRODUCT_DATA_DIR / "bank_account_details" / "response_v1" / "complete.json",
            encoding="utf-8",
        )
    )
    return Page(
        BankAccountDetailsV1Document, json_data["document"]["inference"]["pages"][0]
    )


def test_complete_doc(
    complete_doc: Document[
        BankAccountDetailsV1Document, Page[BankAccountDetailsV1Document]
    ]
):
    reference_str = open(
        PRODUCT_DATA_DIR / "bank_account_details" / "response_v1" / "summary_full.rst",
        "r",
        encoding="utf-8",
    ).read()
    assert str(complete_doc) == reference_str


def test_empty_doc(
    empty_doc: Document[
        BankAccountDetailsV1Document, Page[BankAccountDetailsV1Document]
    ]
):
    prediction = empty_doc.inference.prediction
    assert prediction.iban.value is None
    assert prediction.account_holder_name.value is None
    assert prediction.swift.value is None
