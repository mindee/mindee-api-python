import json

import pytest

from mindee.parsing.common.document import Document
from mindee.parsing.common.page import Page
from mindee.product.fr import BankAccountDetailsV1
from mindee.product.fr.bank_account_details.bank_account_details_v1_document import (
    BankAccountDetailsV1Document,
)
from tests.product import PRODUCT_DATA_DIR

RESPONSE_DIR = PRODUCT_DATA_DIR / "bank_account_details" / "response_v1"

BankAccountDetailsV1DocumentType = Document[
    BankAccountDetailsV1Document,
    Page[BankAccountDetailsV1Document],
]


@pytest.fixture
def complete_doc() -> BankAccountDetailsV1DocumentType:
    file_path = RESPONSE_DIR / "complete.json"
    with open(file_path, "r", encoding="utf-8") as open_file:
        json_data = json.load(open_file)
    return Document(BankAccountDetailsV1, json_data["document"])


@pytest.fixture
def empty_doc() -> BankAccountDetailsV1DocumentType:
    file_path = RESPONSE_DIR / "empty.json"
    with open(file_path, "r", encoding="utf-8") as open_file:
        json_data = json.load(open_file)
    return Document(BankAccountDetailsV1, json_data["document"])


def test_complete_doc(complete_doc: BankAccountDetailsV1DocumentType):
    file_path = RESPONSE_DIR / "summary_full.rst"
    with open(file_path, "r", encoding="utf-8") as open_file:
        reference_str = open_file.read()
    assert str(complete_doc) == reference_str


def test_empty_doc(empty_doc: BankAccountDetailsV1DocumentType):
    prediction = empty_doc.inference.prediction
    assert prediction.iban.value is None
    assert prediction.account_holder_name.value is None
    assert prediction.swift.value is None
