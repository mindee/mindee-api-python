import json

import pytest

from mindee.parsing.common.document import Document
from mindee.parsing.common.page import Page
from mindee.product.driver_license.driver_license_v1 import DriverLicenseV1
from mindee.product.driver_license.driver_license_v1_document import (
    DriverLicenseV1Document,
)
from tests.product import PRODUCT_DATA_DIR

RESPONSE_DIR = PRODUCT_DATA_DIR / "driver_license" / "response_v1"

DriverLicenseV1DocumentType = Document[
    DriverLicenseV1Document,
    Page[DriverLicenseV1Document],
]


@pytest.fixture
def complete_doc() -> DriverLicenseV1DocumentType:
    file_path = RESPONSE_DIR / "complete.json"
    with open(file_path, "r", encoding="utf-8") as open_file:
        json_data = json.load(open_file)
    return Document(DriverLicenseV1, json_data["document"])


@pytest.fixture
def empty_doc() -> DriverLicenseV1DocumentType:
    file_path = RESPONSE_DIR / "empty.json"
    with open(file_path, "r", encoding="utf-8") as open_file:
        json_data = json.load(open_file)
    return Document(DriverLicenseV1, json_data["document"])


def test_complete_doc(complete_doc: DriverLicenseV1DocumentType):
    file_path = RESPONSE_DIR / "summary_full.rst"
    with open(file_path, "r", encoding="utf-8") as open_file:
        reference_str = open_file.read()
    assert str(complete_doc) == reference_str


def test_empty_doc(empty_doc: DriverLicenseV1DocumentType):
    prediction = empty_doc.inference.prediction
    assert prediction.country_code.value is None
    assert prediction.state.value is None
    assert prediction.id.value is None
    assert prediction.category.value is None
    assert prediction.last_name.value is None
    assert prediction.first_name.value is None
    assert prediction.date_of_birth.value is None
    assert prediction.place_of_birth.value is None
    assert prediction.expiry_date.value is None
    assert prediction.issued_date.value is None
    assert prediction.issuing_authority.value is None
    assert prediction.mrz.value is None
    assert prediction.dd_number.value is None
