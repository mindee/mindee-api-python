import json

import pytest

from mindee.parsing.common.document import Document
from mindee.parsing.common.page import Page
from mindee.product import MultiReceiptsDetectorV1
from mindee.product.multi_receipts_detector.multi_receipts_detector_v1_document import (
    MultiReceiptsDetectorV1Document,
)
from tests.product import PRODUCT_DATA_DIR


@pytest.fixture
def complete_doc() -> (
    Document[MultiReceiptsDetectorV1Document, Page[MultiReceiptsDetectorV1Document]]
):
    json_data = json.load(
        open(
            PRODUCT_DATA_DIR
            / "multi_receipts_detector"
            / "response_v1"
            / "complete.json",
            encoding="utf-8",
        )
    )
    return Document(MultiReceiptsDetectorV1, json_data["document"])


@pytest.fixture
def empty_doc() -> (
    Document[MultiReceiptsDetectorV1Document, Page[MultiReceiptsDetectorV1Document]]
):
    json_data = json.load(
        open(
            PRODUCT_DATA_DIR / "multi_receipts_detector" / "response_v1" / "empty.json",
            encoding="utf-8",
        )
    )
    return Document(MultiReceiptsDetectorV1, json_data["document"])


@pytest.fixture
def complete_page_0() -> Page[MultiReceiptsDetectorV1Document]:
    json_data = json.load(
        open(
            PRODUCT_DATA_DIR
            / "multi_receipts_detector"
            / "response_v1"
            / "complete.json",
            encoding="utf-8",
        )
    )
    return Page(
        MultiReceiptsDetectorV1Document, json_data["document"]["inference"]["pages"][0]
    )


def test_complete_doc(
    complete_doc: Document[
        MultiReceiptsDetectorV1Document, Page[MultiReceiptsDetectorV1Document]
    ]
):
    reference_str = open(
        PRODUCT_DATA_DIR
        / "multi_receipts_detector"
        / "response_v1"
        / "summary_full.rst",
        "r",
        encoding="utf-8",
    ).read()
    assert str(complete_doc) == reference_str


def test_empty_doc(
    empty_doc: Document[
        MultiReceiptsDetectorV1Document, Page[MultiReceiptsDetectorV1Document]
    ]
):
    prediction = empty_doc.inference.prediction
    assert len(prediction.receipts) == 0
