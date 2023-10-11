import json

import pytest

from mindee.parsing.common.document import Document
from mindee.parsing.common.page import Page
from mindee.product import CropperV1
from mindee.product.cropper.cropper_v1_document import CropperV1Document
from mindee.product.cropper.cropper_v1_page import CropperV1Page
from tests.product import PRODUCT_DATA_DIR


@pytest.fixture
def complete_doc() -> Document[CropperV1Document, Page[CropperV1Page]]:
    json_data = json.load(
        open(
            PRODUCT_DATA_DIR / "cropper" / "response_v1" / "complete.json",
            encoding="utf-8",
        )
    )
    return Document(CropperV1, json_data["document"])


@pytest.fixture
def empty_doc() -> Document[CropperV1Document, Page[CropperV1Page]]:
    json_data = json.load(
        open(
            PRODUCT_DATA_DIR / "cropper" / "response_v1" / "empty.json",
            encoding="utf-8",
        )
    )
    return Document(CropperV1, json_data["document"])


@pytest.fixture
def complete_page_0() -> Page[CropperV1Page]:
    json_data = json.load(
        open(
            PRODUCT_DATA_DIR / "cropper" / "response_v1" / "complete.json",
            encoding="utf-8",
        )
    )
    return Page(CropperV1Page, json_data["document"]["inference"]["pages"][0])


def test_complete_doc(complete_doc: Document[CropperV1Document, Page[CropperV1Page]]):
    reference_str = open(
        PRODUCT_DATA_DIR / "cropper" / "response_v1" / "summary_full.rst",
        "r",
        encoding="utf-8",
    ).read()
    assert str(complete_doc) == reference_str


def test_empty_doc(empty_doc: Document[CropperV1Document, Page[CropperV1Page]]):
    prediction = empty_doc.inference.pages[0].prediction
    assert len(prediction.cropping) == 0


def test_complete_page_0(complete_page_0: Page[CropperV1Page]):
    reference_str = open(
        PRODUCT_DATA_DIR / "cropper" / "response_v1" / "summary_page0.rst",
        "r",
        encoding="utf-8",
    ).read()
    assert complete_page_0.id == 0
    assert str(complete_page_0) == reference_str
