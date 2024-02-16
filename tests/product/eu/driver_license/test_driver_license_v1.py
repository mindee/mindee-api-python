import json

import pytest

from mindee.parsing.common.document import Document
from mindee.parsing.common.page import Page
from mindee.product.eu import DriverLicenseV1
from mindee.product.eu.driver_license.driver_license_v1_document import (
    DriverLicenseV1Document,
)
from mindee.product.eu.driver_license.driver_license_v1_page import DriverLicenseV1Page
from tests.product import PRODUCT_DATA_DIR


@pytest.fixture
def complete_doc() -> Document[DriverLicenseV1Document, Page[DriverLicenseV1Page]]:
    json_data = json.load(
        open(
            PRODUCT_DATA_DIR / "eu_driver_license" / "response_v1" / "complete.json",
            encoding="utf-8",
        )
    )
    return Document(DriverLicenseV1, json_data["document"])


@pytest.fixture
def empty_doc() -> Document[DriverLicenseV1Document, Page[DriverLicenseV1Page]]:
    json_data = json.load(
        open(
            PRODUCT_DATA_DIR / "eu_driver_license" / "response_v1" / "empty.json",
            encoding="utf-8",
        )
    )
    return Document(DriverLicenseV1, json_data["document"])


@pytest.fixture
def complete_page_0() -> Page[DriverLicenseV1Page]:
    json_data = json.load(
        open(
            PRODUCT_DATA_DIR / "eu_driver_license" / "response_v1" / "complete.json",
            encoding="utf-8",
        )
    )
    return Page(DriverLicenseV1Page, json_data["document"]["inference"]["pages"][0])


def test_complete_doc(
    complete_doc: Document[DriverLicenseV1Document, Page[DriverLicenseV1Page]]
):
    reference_str = open(
        PRODUCT_DATA_DIR / "eu_driver_license" / "response_v1" / "summary_full.rst",
        "r",
        encoding="utf-8",
    ).read()
    assert str(complete_doc) == reference_str


def test_empty_doc(
    empty_doc: Document[DriverLicenseV1Document, Page[DriverLicenseV1Page]]
):
    prediction = empty_doc.inference.prediction
    assert prediction.country_code.value is None
    assert prediction.document_id.value is None
    assert prediction.category.value is None
    assert prediction.last_name.value is None
    assert prediction.first_name.value is None
    assert prediction.date_of_birth.value is None
    assert prediction.place_of_birth.value is None
    assert prediction.expiry_date.value is None
    assert prediction.issue_date.value is None
    assert prediction.issue_authority.value is None
    assert prediction.mrz.value is None
    assert prediction.address.value is None


def test_complete_page_0(complete_page_0: Page[DriverLicenseV1Page]):
    reference_str = open(
        PRODUCT_DATA_DIR / "eu_driver_license" / "response_v1" / "summary_page0.rst",
        "r",
        encoding="utf-8",
    ).read()
    assert complete_page_0.id == 0
    assert str(complete_page_0) == reference_str
