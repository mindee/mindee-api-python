import json

import pytest

from mindee.parsing.common.document import Document
from mindee.parsing.common.page import Page
from mindee.product.us import W9V1
from mindee.product.us.w9.w9_v1_document import W9V1Document
from mindee.product.us.w9.w9_v1_page import W9V1Page
from tests.product import PRODUCT_DATA_DIR


@pytest.fixture
def complete_doc() -> Document[W9V1Document, Page[W9V1Page]]:
    json_data = json.load(
        open(
            PRODUCT_DATA_DIR / "us_w9" / "response_v1" / "complete.json",
            encoding="utf-8",
        )
    )
    return Document(W9V1, json_data["document"])


@pytest.fixture
def empty_doc() -> Document[W9V1Document, Page[W9V1Page]]:
    json_data = json.load(
        open(
            PRODUCT_DATA_DIR / "us_w9" / "response_v1" / "empty.json",
            encoding="utf-8",
        )
    )
    return Document(W9V1, json_data["document"])


@pytest.fixture
def complete_page_0() -> Page[W9V1Page]:
    json_data = json.load(
        open(
            PRODUCT_DATA_DIR / "us_w9" / "response_v1" / "complete.json",
            encoding="utf-8",
        )
    )
    return Page(W9V1Page, json_data["document"]["inference"]["pages"][0])


def test_complete_doc(complete_doc: Document[W9V1Document, Page[W9V1Page]]):
    reference_str = open(
        PRODUCT_DATA_DIR / "us_w9" / "response_v1" / "summary_full.rst",
        "r",
        encoding="utf-8",
    ).read()
    assert str(complete_doc) == reference_str


def test_empty_doc(empty_doc: Document[W9V1Document, Page[W9V1Page]]):
    prediction = empty_doc.inference.pages[0].prediction
    assert prediction.name.value is None
    assert prediction.ssn.value is None
    assert prediction.address.value is None
    assert prediction.city_state_zip.value is None
    assert prediction.business_name.value is None
    assert prediction.ein.value is None
    assert prediction.tax_classification.value is None
    assert prediction.tax_classification_other_details.value is None
    assert prediction.w9_revision_date.value is None
    assert not prediction.signature_position.polygon
    assert not prediction.signature_date_position.polygon
    assert prediction.tax_classification_llc.value is None


def test_complete_page_0(complete_page_0: Page[W9V1Page]):
    reference_str = open(
        PRODUCT_DATA_DIR / "us_w9" / "response_v1" / "summary_page0.rst",
        "r",
        encoding="utf-8",
    ).read()
    assert complete_page_0.id == 0
    assert str(complete_page_0) == reference_str
