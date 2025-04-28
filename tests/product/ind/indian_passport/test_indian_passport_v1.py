import json

import pytest

from mindee.parsing.common.document import Document
from mindee.parsing.common.page import Page
from mindee.product.ind.indian_passport.indian_passport_v1 import IndianPassportV1
from mindee.product.ind.indian_passport.indian_passport_v1_document import (
    IndianPassportV1Document,
)
from tests.product import PRODUCT_DATA_DIR

RESPONSE_DIR = PRODUCT_DATA_DIR / "ind_passport" / "response_v1"

IndianPassportV1DocumentType = Document[
    IndianPassportV1Document,
    Page[IndianPassportV1Document],
]


@pytest.fixture
def complete_doc() -> IndianPassportV1DocumentType:
    file_path = RESPONSE_DIR / "complete.json"
    with open(file_path, "r", encoding="utf-8") as open_file:
        json_data = json.load(open_file)
    return Document(IndianPassportV1, json_data["document"])


@pytest.fixture
def empty_doc() -> IndianPassportV1DocumentType:
    file_path = RESPONSE_DIR / "empty.json"
    with open(file_path, "r", encoding="utf-8") as open_file:
        json_data = json.load(open_file)
    return Document(IndianPassportV1, json_data["document"])


def test_complete_doc(complete_doc: IndianPassportV1DocumentType):
    file_path = RESPONSE_DIR / "summary_full.rst"
    with open(file_path, "r", encoding="utf-8") as open_file:
        reference_str = open_file.read()
    assert str(complete_doc) == reference_str


def test_empty_doc(empty_doc: IndianPassportV1DocumentType):
    prediction = empty_doc.inference.prediction
    assert prediction.country.value is None
    assert prediction.id_number.value is None
    assert prediction.given_names.value is None
    assert prediction.surname.value is None
    assert prediction.birth_date.value is None
    assert prediction.birth_place.value is None
    assert prediction.issuance_place.value is None
    assert prediction.issuance_date.value is None
    assert prediction.expiry_date.value is None
    assert prediction.mrz1.value is None
    assert prediction.mrz2.value is None
    assert prediction.legal_guardian.value is None
    assert prediction.name_of_spouse.value is None
    assert prediction.name_of_mother.value is None
    assert prediction.old_passport_date_of_issue.value is None
    assert prediction.old_passport_number.value is None
    assert prediction.old_passport_place_of_issue.value is None
    assert prediction.address1.value is None
    assert prediction.address2.value is None
    assert prediction.address3.value is None
    assert prediction.file_number.value is None
