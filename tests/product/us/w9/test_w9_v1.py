import json

import pytest

from mindee.parsing.common.document import Document
from mindee.parsing.common.page import Page
from mindee.product.us import W9V1
from mindee.product.us.w9.w9_v1_document import (
    W9V1Document,
)
from mindee.product.us.w9.w9_v1_page import (
    W9V1Page,
)
from tests.product import PRODUCT_DATA_DIR

RESPONSE_DIR = PRODUCT_DATA_DIR / "us_w9" / "response_v1"

W9V1DocumentType = Document[
    W9V1Document,
    Page[W9V1Page],
]


@pytest.fixture
def complete_doc() -> W9V1DocumentType:
    file_path = RESPONSE_DIR / "complete.json"
    with open(file_path, "r", encoding="utf-8") as open_file:
        json_data = json.load(open_file)
    return Document(W9V1, json_data["document"])


@pytest.fixture
def empty_doc() -> W9V1DocumentType:
    file_path = RESPONSE_DIR / "empty.json"
    with open(file_path, "r", encoding="utf-8") as open_file:
        json_data = json.load(open_file)
    return Document(W9V1, json_data["document"])


@pytest.fixture
def complete_page0() -> Page[W9V1Page]:
    file_path = RESPONSE_DIR / "complete.json"
    with open(file_path, "r", encoding="utf-8") as open_file:
        json_data = json.load(open_file)
    page0 = json_data["document"]["inference"]["pages"][0]
    return Page(W9V1Page, page0)


def test_complete_doc(complete_doc: W9V1DocumentType):
    file_path = RESPONSE_DIR / "summary_full.rst"
    with open(file_path, "r", encoding="utf-8") as open_file:
        reference_str = open_file.read()
    assert str(complete_doc) == reference_str


def test_empty_doc(empty_doc: W9V1DocumentType):
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


def test_complete_page0(complete_page0: Page[W9V1Page]):
    file_path = RESPONSE_DIR / "summary_page0.rst"
    with open(file_path, "r", encoding="utf-8") as open_file:
        reference_str = open_file.read()
    assert complete_page0.id == 0
    assert str(complete_page0) == reference_str
