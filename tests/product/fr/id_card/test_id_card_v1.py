import json

import pytest

from mindee.parsing.common.document import Document
from mindee.parsing.common.page import Page
from mindee.product.fr import IdCardV1
from mindee.product.fr.id_card.id_card_v1_document import (
    IdCardV1Document,
)
from mindee.product.fr.id_card.id_card_v1_page import (
    IdCardV1Page,
)
from tests.product import PRODUCT_DATA_DIR

RESPONSE_DIR = PRODUCT_DATA_DIR / "idcard_fr" / "response_v1"

IdCardV1DocumentType = Document[
    IdCardV1Document,
    Page[IdCardV1Page],
]


@pytest.fixture
def complete_doc() -> IdCardV1DocumentType:
    file_path = RESPONSE_DIR / "complete.json"
    with open(file_path, "r", encoding="utf-8") as open_file:
        json_data = json.load(open_file)
    return Document(IdCardV1, json_data["document"])


@pytest.fixture
def empty_doc() -> IdCardV1DocumentType:
    file_path = RESPONSE_DIR / "empty.json"
    with open(file_path, "r", encoding="utf-8") as open_file:
        json_data = json.load(open_file)
    return Document(IdCardV1, json_data["document"])


@pytest.fixture
def complete_page0() -> Page[IdCardV1Page]:
    file_path = RESPONSE_DIR / "complete.json"
    with open(file_path, "r", encoding="utf-8") as open_file:
        json_data = json.load(open_file)
    page0 = json_data["document"]["inference"]["pages"][0]
    return Page(IdCardV1Page, page0)


def test_complete_doc(complete_doc: IdCardV1DocumentType):
    file_path = RESPONSE_DIR / "summary_full.rst"
    with open(file_path, "r", encoding="utf-8") as open_file:
        reference_str = open_file.read()
    assert str(complete_doc) == reference_str


def test_empty_doc(empty_doc: IdCardV1DocumentType):
    prediction = empty_doc.inference.prediction
    assert prediction.id_number.value is None
    assert len(prediction.given_names) == 0
    assert prediction.surname.value is None
    assert prediction.birth_date.value is None
    assert prediction.birth_place.value is None
    assert prediction.expiry_date.value is None
    assert prediction.authority.value is None
    assert prediction.gender.value is None
    assert prediction.mrz1.value is None
    assert prediction.mrz2.value is None


def test_complete_page0(complete_page0: Page[IdCardV1Page]):
    file_path = RESPONSE_DIR / "summary_page0.rst"
    with open(file_path, "r", encoding="utf-8") as open_file:
        reference_str = open_file.read()
    assert complete_page0.id == 0
    assert str(complete_page0) == reference_str
