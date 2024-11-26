import json

import pytest

from mindee.parsing.common.document import Document
from mindee.parsing.common.page import Page
from mindee.product.fr.health_card.health_card_v1 import HealthCardV1
from mindee.product.fr.health_card.health_card_v1_document import (
    HealthCardV1Document,
)
from tests.product import PRODUCT_DATA_DIR

RESPONSE_DIR = PRODUCT_DATA_DIR / "french_healthcard" / "response_v1"

HealthCardV1DocumentType = Document[
    HealthCardV1Document,
    Page[HealthCardV1Document],
]


@pytest.fixture
def complete_doc() -> HealthCardV1DocumentType:
    file_path = RESPONSE_DIR / "complete.json"
    with open(file_path, "r", encoding="utf-8") as open_file:
        json_data = json.load(open_file)
    return Document(HealthCardV1, json_data["document"])


@pytest.fixture
def empty_doc() -> HealthCardV1DocumentType:
    file_path = RESPONSE_DIR / "empty.json"
    with open(file_path, "r", encoding="utf-8") as open_file:
        json_data = json.load(open_file)
    return Document(HealthCardV1, json_data["document"])


def test_complete_doc(complete_doc: HealthCardV1DocumentType):
    file_path = RESPONSE_DIR / "summary_full.rst"
    with open(file_path, "r", encoding="utf-8") as open_file:
        reference_str = open_file.read()
    assert str(complete_doc) == reference_str


def test_empty_doc(empty_doc: HealthCardV1DocumentType):
    prediction = empty_doc.inference.prediction
    assert len(prediction.given_names) == 0
    assert prediction.surname.value is None
    assert prediction.social_security.value is None
    assert prediction.issuance_date.value is None
