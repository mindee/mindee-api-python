import json

import pytest

from mindee.parsing.common.document import Document
from mindee.parsing.common.page import Page
from mindee.product import PassportV1
from mindee.product.passport.passport_v1_document import PassportV1Document
from tests.product import PRODUCT_DATA_DIR


@pytest.fixture
def complete_doc() -> Document[PassportV1Document, Page[PassportV1Document]]:
    json_data = json.load(
        open(
            PRODUCT_DATA_DIR / "passport" / "response_v1" / "complete.json",
            encoding="utf-8",
        )
    )
    return Document(PassportV1, json_data["document"])


@pytest.fixture
def empty_doc() -> Document[PassportV1Document, Page[PassportV1Document]]:
    json_data = json.load(
        open(
            PRODUCT_DATA_DIR / "passport" / "response_v1" / "empty.json",
            encoding="utf-8",
        )
    )
    return Document(PassportV1, json_data["document"])


@pytest.fixture
def complete_page_0() -> Page[PassportV1Document]:
    json_data = json.load(
        open(
            PRODUCT_DATA_DIR / "passport" / "response_v1" / "complete.json",
            encoding="utf-8",
        )
    )
    return Page(PassportV1Document, json_data["document"]["inference"]["pages"][0])


def test_complete_doc(
    complete_doc: Document[PassportV1Document, Page[PassportV1Document]]
):
    reference_str = open(
        PRODUCT_DATA_DIR / "passport" / "response_v1" / "summary_full.rst",
        "r",
        encoding="utf-8",
    ).read()
    assert str(complete_doc) == reference_str


def test_empty_doc(empty_doc: Document[PassportV1Document, Page[PassportV1Document]]):
    prediction = empty_doc.inference.prediction
    assert prediction.country.value is None
    assert prediction.id_number.value is None
    assert len(prediction.given_names) == 0
    assert prediction.surname.value is None
    assert prediction.birth_date.value is None
    assert prediction.birth_place.value is None
    assert prediction.gender.value is None
    assert prediction.issuance_date.value is None
    assert prediction.expiry_date.value is None
    assert prediction.mrz1.value is None
    assert prediction.mrz2.value is None
