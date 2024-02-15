import json

import pytest

from mindee.parsing.common.document import Document
from mindee.parsing.common.page import Page
from mindee.product import InternationalIdV2
from mindee.product.international_id.international_id_v2_document import (
    InternationalIdV2Document,
)
from tests.product import PRODUCT_DATA_DIR


@pytest.fixture
def complete_doc() -> (
    Document[InternationalIdV2Document, Page[InternationalIdV2Document]]
):
    json_data = json.load(
        open(
            PRODUCT_DATA_DIR / "international_id" / "response_v2" / "complete.json",
            encoding="utf-8",
        )
    )
    return Document(InternationalIdV2, json_data["document"])


@pytest.fixture
def empty_doc() -> Document[InternationalIdV2Document, Page[InternationalIdV2Document]]:
    json_data = json.load(
        open(
            PRODUCT_DATA_DIR / "international_id" / "response_v2" / "empty.json",
            encoding="utf-8",
        )
    )
    return Document(InternationalIdV2, json_data["document"])


@pytest.fixture
def complete_page_0() -> Page[InternationalIdV2Document]:
    json_data = json.load(
        open(
            PRODUCT_DATA_DIR / "international_id" / "response_v2" / "complete.json",
            encoding="utf-8",
        )
    )
    return Page(
        InternationalIdV2Document, json_data["document"]["inference"]["pages"][0]
    )


def test_complete_doc(
    complete_doc: Document[InternationalIdV2Document, Page[InternationalIdV2Document]]
):
    reference_str = open(
        PRODUCT_DATA_DIR / "international_id" / "response_v2" / "summary_full.rst",
        "r",
        encoding="utf-8",
    ).read()
    assert str(complete_doc) == reference_str


def test_empty_doc(
    empty_doc: Document[InternationalIdV2Document, Page[InternationalIdV2Document]]
):
    prediction = empty_doc.inference.prediction
    assert prediction.document_number.value is None
    assert len(prediction.surnames) == 0
    assert len(prediction.given_names) == 0
    assert prediction.sex.value is None
    assert prediction.birth_date.value is None
    assert prediction.birth_place.value is None
    assert prediction.nationality.value is None
    assert prediction.personal_number.value is None
    assert prediction.country_of_issue.value is None
    assert prediction.state_of_issue.value is None
    assert prediction.issue_date.value is None
    assert prediction.expiry_date.value is None
    assert prediction.address.value is None
    assert prediction.mrz_line1.value is None
    assert prediction.mrz_line2.value is None
    assert prediction.mrz_line3.value is None
