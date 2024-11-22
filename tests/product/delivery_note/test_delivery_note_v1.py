import json

import pytest

from mindee.parsing.common.document import Document
from mindee.parsing.common.page import Page
from mindee.product.delivery_note.delivery_note_v1 import DeliveryNoteV1
from mindee.product.delivery_note.delivery_note_v1_document import (
    DeliveryNoteV1Document,
)
from tests.product import PRODUCT_DATA_DIR

RESPONSE_DIR = PRODUCT_DATA_DIR / "delivery_notes" / "response_v1"

DeliveryNoteV1DocumentType = Document[
    DeliveryNoteV1Document,
    Page[DeliveryNoteV1Document],
]


@pytest.fixture
def complete_doc() -> DeliveryNoteV1DocumentType:
    file_path = RESPONSE_DIR / "complete.json"
    with open(file_path, "r", encoding="utf-8") as open_file:
        json_data = json.load(open_file)
    return Document(DeliveryNoteV1, json_data["document"])


@pytest.fixture
def empty_doc() -> DeliveryNoteV1DocumentType:
    file_path = RESPONSE_DIR / "empty.json"
    with open(file_path, "r", encoding="utf-8") as open_file:
        json_data = json.load(open_file)
    return Document(DeliveryNoteV1, json_data["document"])


def test_complete_doc(complete_doc: DeliveryNoteV1DocumentType):
    file_path = RESPONSE_DIR / "summary_full.rst"
    with open(file_path, "r", encoding="utf-8") as open_file:
        reference_str = open_file.read()
    assert str(complete_doc) == reference_str


def test_empty_doc(empty_doc: DeliveryNoteV1DocumentType):
    prediction = empty_doc.inference.prediction
    assert prediction.delivery_date.value is None
    assert prediction.delivery_number.value is None
    assert prediction.supplier_name.value is None
    assert prediction.supplier_address.value is None
    assert prediction.customer_name.value is None
    assert prediction.customer_address.value is None
    assert prediction.total_amount.value is None
