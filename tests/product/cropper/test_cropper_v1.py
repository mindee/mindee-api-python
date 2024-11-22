import json

import pytest

from mindee.parsing.common.document import Document
from mindee.parsing.common.page import Page
from mindee.product.cropper.cropper_v1 import CropperV1
from mindee.product.cropper.cropper_v1_document import (
    CropperV1Document,
)
from mindee.product.cropper.cropper_v1_page import (
    CropperV1Page,
)
from tests.product import PRODUCT_DATA_DIR

RESPONSE_DIR = PRODUCT_DATA_DIR / "cropper" / "response_v1"

CropperV1DocumentType = Document[
    CropperV1Document,
    Page[CropperV1Page],
]


@pytest.fixture
def complete_doc() -> CropperV1DocumentType:
    file_path = RESPONSE_DIR / "complete.json"
    with open(file_path, "r", encoding="utf-8") as open_file:
        json_data = json.load(open_file)
    return Document(CropperV1, json_data["document"])


@pytest.fixture
def empty_doc() -> CropperV1DocumentType:
    file_path = RESPONSE_DIR / "empty.json"
    with open(file_path, "r", encoding="utf-8") as open_file:
        json_data = json.load(open_file)
    return Document(CropperV1, json_data["document"])


@pytest.fixture
def complete_page0() -> Page[CropperV1Page]:
    file_path = RESPONSE_DIR / "complete.json"
    with open(file_path, "r", encoding="utf-8") as open_file:
        json_data = json.load(open_file)
    page0 = json_data["document"]["inference"]["pages"][0]
    return Page(CropperV1Page, page0)


def test_complete_doc(complete_doc: CropperV1DocumentType):
    file_path = RESPONSE_DIR / "summary_full.rst"
    with open(file_path, "r", encoding="utf-8") as open_file:
        reference_str = open_file.read()
    assert str(complete_doc) == reference_str


def test_empty_doc(empty_doc: CropperV1DocumentType):
    prediction = empty_doc.inference.pages[0].prediction
    assert len(prediction.cropping) == 0


def test_complete_page0(complete_page0: Page[CropperV1Page]):
    file_path = RESPONSE_DIR / "summary_page0.rst"
    with open(file_path, "r", encoding="utf-8") as open_file:
        reference_str = open_file.read()
    assert complete_page0.id == 0
    assert str(complete_page0) == reference_str
