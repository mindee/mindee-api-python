import json

import pytest

from mindee.parsing.common.document import Document
from mindee.parsing.common.page import Page
from mindee.product.us.healthcare_card.healthcare_card_v1 import HealthcareCardV1
from mindee.product.us.healthcare_card.healthcare_card_v1_document import (
    HealthcareCardV1Document,
)
from tests.product import PRODUCT_DATA_DIR

RESPONSE_DIR = PRODUCT_DATA_DIR / "us_healthcare_cards" / "response_v1"

HealthcareCardV1DocumentType = Document[
    HealthcareCardV1Document,
    Page[HealthcareCardV1Document],
]


@pytest.fixture
def complete_doc() -> HealthcareCardV1DocumentType:
    file_path = RESPONSE_DIR / "complete.json"
    with open(file_path, "r", encoding="utf-8") as open_file:
        json_data = json.load(open_file)
    return Document(HealthcareCardV1, json_data["document"])


@pytest.fixture
def empty_doc() -> HealthcareCardV1DocumentType:
    file_path = RESPONSE_DIR / "empty.json"
    with open(file_path, "r", encoding="utf-8") as open_file:
        json_data = json.load(open_file)
    return Document(HealthcareCardV1, json_data["document"])


def test_complete_doc(complete_doc: HealthcareCardV1DocumentType):
    file_path = RESPONSE_DIR / "summary_full.rst"
    with open(file_path, "r", encoding="utf-8") as open_file:
        reference_str = open_file.read()
    assert str(complete_doc) == reference_str


def test_empty_doc(empty_doc: HealthcareCardV1DocumentType):
    prediction = empty_doc.inference.prediction
    assert prediction.company_name.value is None
    assert prediction.plan_name.value is None
    assert prediction.member_name.value is None
    assert prediction.member_id.value is None
    assert prediction.issuer_80840.value is None
    assert len(prediction.dependents) == 0
    assert prediction.group_number.value is None
    assert prediction.payer_id.value is None
    assert prediction.rx_bin.value is None
    assert prediction.rx_id.value is None
    assert prediction.rx_grp.value is None
    assert prediction.rx_pcn.value is None
    assert len(prediction.copays) == 0
    assert prediction.enrollment_date.value is None
