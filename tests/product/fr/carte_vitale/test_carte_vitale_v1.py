import json

import pytest

from mindee.parsing.common.document import Document
from mindee.parsing.common.page import Page
from mindee.product.fr import CarteVitaleV1
from mindee.product.fr.carte_vitale.carte_vitale_v1_document import (
    CarteVitaleV1Document,
)
from tests.product import PRODUCT_DATA_DIR


@pytest.fixture
def complete_doc() -> Document[CarteVitaleV1Document, Page[CarteVitaleV1Document]]:
    json_data = json.load(
        open(
            PRODUCT_DATA_DIR / "carte_vitale" / "response_v1" / "complete.json",
            encoding="utf-8",
        )
    )
    return Document(CarteVitaleV1, json_data["document"])


@pytest.fixture
def empty_doc() -> Document[CarteVitaleV1Document, Page[CarteVitaleV1Document]]:
    json_data = json.load(
        open(
            PRODUCT_DATA_DIR / "carte_vitale" / "response_v1" / "empty.json",
            encoding="utf-8",
        )
    )
    return Document(CarteVitaleV1, json_data["document"])


@pytest.fixture
def complete_page_0() -> Page[CarteVitaleV1Document]:
    json_data = json.load(
        open(
            PRODUCT_DATA_DIR / "carte_vitale" / "response_v1" / "complete.json",
            encoding="utf-8",
        )
    )
    return Page(CarteVitaleV1Document, json_data["document"]["inference"]["pages"][0])


def test_complete_doc(
    complete_doc: Document[CarteVitaleV1Document, Page[CarteVitaleV1Document]]
):
    reference_str = open(
        PRODUCT_DATA_DIR / "carte_vitale" / "response_v1" / "summary_full.rst",
        "r",
        encoding="utf-8",
    ).read()
    assert str(complete_doc) == reference_str


def test_empty_doc(
    empty_doc: Document[CarteVitaleV1Document, Page[CarteVitaleV1Document]]
):
    prediction = empty_doc.inference.prediction
    assert len(prediction.given_names) == 0
    assert prediction.surname.value is None
    assert prediction.social_security.value is None
    assert prediction.issuance_date.value is None
