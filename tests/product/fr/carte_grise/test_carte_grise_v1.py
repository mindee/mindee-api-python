import json

import pytest

from mindee.parsing.common.document import Document
from mindee.parsing.common.page import Page
from mindee.product.fr import CarteGriseV1
from mindee.product.fr.carte_grise.carte_grise_v1_document import CarteGriseV1Document
from tests.product import PRODUCT_DATA_DIR


@pytest.fixture
def complete_doc() -> Document[CarteGriseV1Document, Page[CarteGriseV1Document]]:
    json_data = json.load(
        open(
            PRODUCT_DATA_DIR / "carte_grise" / "response_v1" / "complete.json",
            encoding="utf-8",
        )
    )
    return Document(CarteGriseV1, json_data["document"])


@pytest.fixture
def empty_doc() -> Document[CarteGriseV1Document, Page[CarteGriseV1Document]]:
    json_data = json.load(
        open(
            PRODUCT_DATA_DIR / "carte_grise" / "response_v1" / "empty.json",
            encoding="utf-8",
        )
    )
    return Document(CarteGriseV1, json_data["document"])


@pytest.fixture
def complete_page_0() -> Page[CarteGriseV1Document]:
    json_data = json.load(
        open(
            PRODUCT_DATA_DIR / "carte_grise" / "response_v1" / "complete.json",
            encoding="utf-8",
        )
    )
    return Page(CarteGriseV1Document, json_data["document"]["inference"]["pages"][0])


def test_complete_doc(
    complete_doc: Document[CarteGriseV1Document, Page[CarteGriseV1Document]]
):
    reference_str = open(
        PRODUCT_DATA_DIR / "carte_grise" / "response_v1" / "summary_full.rst",
        "r",
        encoding="utf-8",
    ).read()
    assert str(complete_doc) == reference_str


def test_empty_doc(
    empty_doc: Document[CarteGriseV1Document, Page[CarteGriseV1Document]]
):
    prediction = empty_doc.inference.prediction
    assert prediction.a.value is None
    assert prediction.b.value is None
    assert prediction.c1.value is None
    assert prediction.c3.value is None
    assert prediction.c41.value is None
    assert prediction.c4a.value is None
    assert prediction.d1.value is None
    assert prediction.d3.value is None
    assert prediction.e.value is None
    assert prediction.f1.value is None
    assert prediction.f2.value is None
    assert prediction.f3.value is None
    assert prediction.g.value is None
    assert prediction.g1.value is None
    assert prediction.i.value is None
    assert prediction.j.value is None
    assert prediction.j1.value is None
    assert prediction.j2.value is None
    assert prediction.j3.value is None
    assert prediction.p1.value is None
    assert prediction.p2.value is None
    assert prediction.p3.value is None
    assert prediction.p6.value is None
    assert prediction.q.value is None
    assert prediction.s1.value is None
    assert prediction.s2.value is None
    assert prediction.u1.value is None
    assert prediction.u2.value is None
    assert prediction.v7.value is None
    assert prediction.x1.value is None
    assert prediction.y1.value is None
    assert prediction.y2.value is None
    assert prediction.y3.value is None
    assert prediction.y4.value is None
    assert prediction.y5.value is None
    assert prediction.y6.value is None
    assert prediction.formula_number.value is None
    assert prediction.owner_first_name.value is None
    assert prediction.owner_surname.value is None
    assert prediction.mrz1.value is None
    assert prediction.mrz2.value is None
