import json

import pytest

from mindee.parsing.common.document import Document
from mindee.parsing.common.page import Page
from mindee.product.fr import IdCardV1
from mindee.product.fr.id_card.id_card_v1_document import IdCardV1Document
from mindee.product.fr.id_card.id_card_v1_page import IdCardV1Page
from tests.product import PRODUCT_DATA_DIR


@pytest.fixture
def complete_doc() -> Document[IdCardV1Document, Page[IdCardV1Page]]:
    json_data = json.load(
        open(
            PRODUCT_DATA_DIR / "idcard_fr" / "response_v1" / "complete.json",
            encoding="utf-8",
        )
    )
    return Document(IdCardV1, json_data["document"])


@pytest.fixture
def empty_doc() -> Document[IdCardV1Document, Page[IdCardV1Page]]:
    json_data = json.load(
        open(
            PRODUCT_DATA_DIR / "idcard_fr" / "response_v1" / "empty.json",
            encoding="utf-8",
        )
    )
    return Document(IdCardV1, json_data["document"])


@pytest.fixture
def complete_page_0() -> Page[IdCardV1Page]:
    json_data = json.load(
        open(
            PRODUCT_DATA_DIR / "idcard_fr" / "response_v1" / "complete.json",
            encoding="utf-8",
        )
    )
    return Page(IdCardV1Page, json_data["document"]["inference"]["pages"][0])


def test_complete_doc(complete_doc: Document[IdCardV1Document, Page[IdCardV1Page]]):
    reference_str = open(
        PRODUCT_DATA_DIR / "idcard_fr" / "response_v1" / "summary_full.rst",
        "r",
        encoding="utf-8",
    ).read()
    assert str(complete_doc) == reference_str


def test_empty_doc(empty_doc: Document[IdCardV1Document, Page[IdCardV1Page]]):
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


def test_complete_page_0(complete_page_0: Page[IdCardV1Page]):
    reference_str = open(
        PRODUCT_DATA_DIR / "idcard_fr" / "response_v1" / "summary_page0.rst",
        "r",
        encoding="utf-8",
    ).read()
    assert complete_page_0.id == 0
    assert str(complete_page_0) == reference_str
