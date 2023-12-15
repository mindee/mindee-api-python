import json

import pytest

from mindee.parsing.common.document import Document
from mindee.parsing.common.page import Page
from mindee.product.fr import BankAccountDetailsV2
from mindee.product.fr.bank_account_details.bank_account_details_v2_document import (
    BankAccountDetailsV2Document,
)
from tests.product import PRODUCT_DATA_DIR


@pytest.fixture
def complete_doc() -> (
    Document[BankAccountDetailsV2Document, Page[BankAccountDetailsV2Document]]
):
    json_data = json.load(
        open(
            PRODUCT_DATA_DIR / "bank_account_details" / "response_v2" / "complete.json",
            encoding="utf-8",
        )
    )
    return Document(BankAccountDetailsV2, json_data["document"])


@pytest.fixture
def empty_doc() -> (
    Document[BankAccountDetailsV2Document, Page[BankAccountDetailsV2Document]]
):
    json_data = json.load(
        open(
            PRODUCT_DATA_DIR / "bank_account_details" / "response_v2" / "empty.json",
            encoding="utf-8",
        )
    )
    return Document(BankAccountDetailsV2, json_data["document"])


@pytest.fixture
def complete_page_0() -> Page[BankAccountDetailsV2Document]:
    json_data = json.load(
        open(
            PRODUCT_DATA_DIR / "bank_account_details" / "response_v2" / "complete.json",
            encoding="utf-8",
        )
    )
    return Page(
        BankAccountDetailsV2Document, json_data["document"]["inference"]["pages"][0]
    )


def test_complete_doc(
    complete_doc: Document[
        BankAccountDetailsV2Document, Page[BankAccountDetailsV2Document]
    ]
):
    reference_str = open(
        PRODUCT_DATA_DIR / "bank_account_details" / "response_v2" / "summary_full.rst",
        "r",
        encoding="utf-8",
    ).read()
    assert str(complete_doc) == reference_str


def test_empty_doc(
    empty_doc: Document[
        BankAccountDetailsV2Document, Page[BankAccountDetailsV2Document]
    ]
):
    prediction = empty_doc.inference.prediction
    assert prediction.account_holders_names.value is None
    assert prediction.bban.bban_bank_code is None
    assert prediction.bban.bban_branch_code is None
    assert prediction.bban.bban_key is None
    assert prediction.bban.bban_number is None
    assert prediction.iban.value is None
    assert prediction.swift_code.value is None
