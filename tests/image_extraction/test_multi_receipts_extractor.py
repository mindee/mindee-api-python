import json
from io import BytesIO

import pytest

from mindee.error import MimeTypeError
from mindee.image_extraction.common import get_image_size
from mindee.image_extraction.multi_receipts_extractor.mult_receipts_extractor import extract_receipts
from mindee.input import PathInput
from mindee.product import MultiReceiptsDetectorV1
from tests.test_inputs import PRODUCT_DATA_DIR


@pytest.fixture
def multi_receipts_single_page_path():
    return PRODUCT_DATA_DIR / "multi_receipts_detector" / "default_sample.jpg"


@pytest.fixture
def multi_receipts_single_page_json_path():
    return PRODUCT_DATA_DIR / "multi_receipts_detector" / "response_v1" / "complete.json"


@pytest.fixture
def multi_receipts_multi_page_path():
    return PRODUCT_DATA_DIR / "multi_receipts_detector" / "multipage_sample.pdf"


@pytest.fixture
def multi_receipts_multi_page_json_path():
    return PRODUCT_DATA_DIR / "multi_receipts_detector" / "response_v1" / "multipage_sample.json"


def test_single_page_multi_receipt_split(multi_receipts_single_page_path, multi_receipts_single_page_json_path):
    input_sample = PathInput(multi_receipts_single_page_path)
    with open(multi_receipts_single_page_json_path, "rb") as f:
        response = json.load(f)
    doc = MultiReceiptsDetectorV1(response["document"]["inference"])
    extracted_receipts = extract_receipts(input_sample, doc)
    assert len(extracted_receipts) == 6
    for i in range(len(extracted_receipts)):
        assert extracted_receipts[i].buffer is not None
        assert extracted_receipts[i].page_id == 0
        assert extracted_receipts[i].receipt_id == i


def test_multi_page_receipt_split(multi_receipts_multi_page_path, multi_receipts_multi_page_json_path):
    input_sample = PathInput(multi_receipts_multi_page_path)
    with open(multi_receipts_multi_page_json_path, "rb") as f:
        response = json.load(f)
    doc = MultiReceiptsDetectorV1(response["document"]["inference"])
    extracted_receipts = extract_receipts(input_sample, doc)
    assert len(extracted_receipts) == 5
    assert extracted_receipts[0].buffer is not None
    assert extracted_receipts[0].page_id == 0
    assert extracted_receipts[0].receipt_id == 0

    assert extracted_receipts[1].buffer is not None
    assert extracted_receipts[1].page_id == 0
    assert extracted_receipts[1].receipt_id == 1

    assert extracted_receipts[2].buffer is not None
    assert extracted_receipts[2].page_id == 0
    assert extracted_receipts[2].receipt_id == 2

    assert extracted_receipts[3].buffer is not None
    assert extracted_receipts[3].page_id == 1
    assert extracted_receipts[3].receipt_id == 0

    assert extracted_receipts[4].buffer is not None
    assert extracted_receipts[4].page_id == 1
    assert extracted_receipts[4].receipt_id == 1



