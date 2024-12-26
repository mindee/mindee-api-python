import json

import pytest

from mindee.parsing.common.document import Document
from mindee.parsing.common.page import Page
from mindee.product.us.us_mail.us_mail_v3 import UsMailV3
from mindee.product.us.us_mail.us_mail_v3_document import (
    UsMailV3Document,
)
from tests.product import PRODUCT_DATA_DIR

RESPONSE_DIR = PRODUCT_DATA_DIR / "us_mail" / "response_v3"

UsMailV3DocumentType = Document[
    UsMailV3Document,
    Page[UsMailV3Document],
]


@pytest.fixture
def complete_doc() -> UsMailV3DocumentType:
    file_path = RESPONSE_DIR / "complete.json"
    with open(file_path, "r", encoding="utf-8") as open_file:
        json_data = json.load(open_file)
    return Document(UsMailV3, json_data["document"])


@pytest.fixture
def empty_doc() -> UsMailV3DocumentType:
    file_path = RESPONSE_DIR / "empty.json"
    with open(file_path, "r", encoding="utf-8") as open_file:
        json_data = json.load(open_file)
    return Document(UsMailV3, json_data["document"])


def test_complete_doc(complete_doc: UsMailV3DocumentType):
    file_path = RESPONSE_DIR / "summary_full.rst"
    with open(file_path, "r", encoding="utf-8") as open_file:
        reference_str = open_file.read()
    assert str(complete_doc) == reference_str


def test_empty_doc(empty_doc: UsMailV3DocumentType):
    prediction = empty_doc.inference.prediction
    assert prediction.sender_name.value is None
    assert prediction.sender_address.city is None
    assert prediction.sender_address.complete is None
    assert prediction.sender_address.postal_code is None
    assert prediction.sender_address.state is None
    assert prediction.sender_address.street is None
    assert len(prediction.recipient_names) == 0
    assert len(prediction.recipient_addresses) == 0
    assert prediction.is_return_to_sender.value is None
