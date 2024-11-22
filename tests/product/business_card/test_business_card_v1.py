import json

import pytest

from mindee.parsing.common.document import Document
from mindee.parsing.common.page import Page
from mindee.product.business_card.business_card_v1 import BusinessCardV1
from mindee.product.business_card.business_card_v1_document import (
    BusinessCardV1Document,
)
from tests.product import PRODUCT_DATA_DIR

RESPONSE_DIR = PRODUCT_DATA_DIR / "business_card" / "response_v1"

BusinessCardV1DocumentType = Document[
    BusinessCardV1Document,
    Page[BusinessCardV1Document],
]


@pytest.fixture
def complete_doc() -> BusinessCardV1DocumentType:
    file_path = RESPONSE_DIR / "complete.json"
    with open(file_path, "r", encoding="utf-8") as open_file:
        json_data = json.load(open_file)
    return Document(BusinessCardV1, json_data["document"])


@pytest.fixture
def empty_doc() -> BusinessCardV1DocumentType:
    file_path = RESPONSE_DIR / "empty.json"
    with open(file_path, "r", encoding="utf-8") as open_file:
        json_data = json.load(open_file)
    return Document(BusinessCardV1, json_data["document"])


def test_complete_doc(complete_doc: BusinessCardV1DocumentType):
    file_path = RESPONSE_DIR / "summary_full.rst"
    with open(file_path, "r", encoding="utf-8") as open_file:
        reference_str = open_file.read()
    assert str(complete_doc) == reference_str


def test_empty_doc(empty_doc: BusinessCardV1DocumentType):
    prediction = empty_doc.inference.prediction
    assert prediction.firstname.value is None
    assert prediction.lastname.value is None
    assert prediction.job_title.value is None
    assert prediction.company.value is None
    assert prediction.email.value is None
    assert prediction.phone_number.value is None
    assert prediction.mobile_number.value is None
    assert prediction.fax_number.value is None
    assert prediction.address.value is None
    assert prediction.website.value is None
    assert len(prediction.social_media) == 0
