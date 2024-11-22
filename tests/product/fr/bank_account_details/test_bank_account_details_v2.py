import json

import pytest

from mindee.parsing.common.document import Document
from mindee.parsing.common.page import Page
from mindee.product.fr.bank_account_details.bank_account_details_v2 import (
    BankAccountDetailsV2,
)
from mindee.product.fr.bank_account_details.bank_account_details_v2_document import (
    BankAccountDetailsV2Document,
)
from tests.product import PRODUCT_DATA_DIR

RESPONSE_DIR = PRODUCT_DATA_DIR / "bank_account_details" / "response_v2"

BankAccountDetailsV2DocumentType = Document[
    BankAccountDetailsV2Document,
    Page[BankAccountDetailsV2Document],
]


@pytest.fixture
def complete_doc() -> BankAccountDetailsV2DocumentType:
    file_path = RESPONSE_DIR / "complete.json"
    with open(file_path, "r", encoding="utf-8") as open_file:
        json_data = json.load(open_file)
    return Document(BankAccountDetailsV2, json_data["document"])


@pytest.fixture
def empty_doc() -> BankAccountDetailsV2DocumentType:
    file_path = RESPONSE_DIR / "empty.json"
    with open(file_path, "r", encoding="utf-8") as open_file:
        json_data = json.load(open_file)
    return Document(BankAccountDetailsV2, json_data["document"])


def test_complete_doc(complete_doc: BankAccountDetailsV2DocumentType):
    file_path = RESPONSE_DIR / "summary_full.rst"
    with open(file_path, "r", encoding="utf-8") as open_file:
        reference_str = open_file.read()
    assert str(complete_doc) == reference_str


def test_empty_doc(empty_doc: BankAccountDetailsV2DocumentType):
    prediction = empty_doc.inference.prediction
    assert prediction.account_holders_names.value is None
    assert prediction.bban.bban_bank_code is None
    assert prediction.bban.bban_branch_code is None
    assert prediction.bban.bban_key is None
    assert prediction.bban.bban_number is None
    assert prediction.iban.value is None
    assert prediction.swift_code.value is None
