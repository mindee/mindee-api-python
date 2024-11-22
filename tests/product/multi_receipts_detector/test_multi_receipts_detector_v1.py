import json

import pytest

from mindee.parsing.common.document import Document
from mindee.parsing.common.page import Page
from mindee.product.multi_receipts_detector.multi_receipts_detector_v1 import (
    MultiReceiptsDetectorV1,
)
from mindee.product.multi_receipts_detector.multi_receipts_detector_v1_document import (
    MultiReceiptsDetectorV1Document,
)
from tests.product import PRODUCT_DATA_DIR

RESPONSE_DIR = PRODUCT_DATA_DIR / "multi_receipts_detector" / "response_v1"

MultiReceiptsDetectorV1DocumentType = Document[
    MultiReceiptsDetectorV1Document,
    Page[MultiReceiptsDetectorV1Document],
]


@pytest.fixture
def complete_doc() -> MultiReceiptsDetectorV1DocumentType:
    file_path = RESPONSE_DIR / "complete.json"
    with open(file_path, "r", encoding="utf-8") as open_file:
        json_data = json.load(open_file)
    return Document(MultiReceiptsDetectorV1, json_data["document"])


@pytest.fixture
def empty_doc() -> MultiReceiptsDetectorV1DocumentType:
    file_path = RESPONSE_DIR / "empty.json"
    with open(file_path, "r", encoding="utf-8") as open_file:
        json_data = json.load(open_file)
    return Document(MultiReceiptsDetectorV1, json_data["document"])


def test_complete_doc(complete_doc: MultiReceiptsDetectorV1DocumentType):
    file_path = RESPONSE_DIR / "summary_full.rst"
    with open(file_path, "r", encoding="utf-8") as open_file:
        reference_str = open_file.read()
    assert str(complete_doc) == reference_str


def test_empty_doc(empty_doc: MultiReceiptsDetectorV1DocumentType):
    prediction = empty_doc.inference.prediction
    assert len(prediction.receipts) == 0
