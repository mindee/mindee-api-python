import json

import pytest
from PIL import Image

from mindee.extraction.multi_receipts_extractor.multi_receipts_extractor import (
    extract_receipts,
)
from mindee.input.sources.path_input import PathInput
from mindee.product.multi_receipts_detector.multi_receipts_detector_v1 import (
    MultiReceiptsDetectorV1,
)
from tests.test_inputs import PRODUCT_DATA_DIR


@pytest.fixture
def multi_receipts_single_page_path():
    return PRODUCT_DATA_DIR / "multi_receipts_detector" / "default_sample.jpg"


@pytest.fixture
def multi_receipts_single_page_json_path():
    return (
        PRODUCT_DATA_DIR / "multi_receipts_detector" / "response_v1" / "complete.json"
    )


@pytest.fixture
def multi_receipts_multi_page_path():
    return PRODUCT_DATA_DIR / "multi_receipts_detector" / "multipage_sample.pdf"


@pytest.fixture
def multi_receipts_multi_page_json_path():
    return (
        PRODUCT_DATA_DIR
        / "multi_receipts_detector"
        / "response_v1"
        / "multipage_sample.json"
    )


def test_single_page_multi_receipt_split(
    multi_receipts_single_page_path, multi_receipts_single_page_json_path
):
    input_sample = PathInput(multi_receipts_single_page_path)
    with open(multi_receipts_single_page_json_path, "rb") as f:
        response = json.load(f)
    doc = MultiReceiptsDetectorV1(response["document"]["inference"])
    extracted_receipts = extract_receipts(input_sample, doc)
    assert len(extracted_receipts) == 6

    assert extracted_receipts[0].page_id == 0
    assert extracted_receipts[0].element_id == 0
    image_buffer_0 = Image.open(extracted_receipts[0].buffer)
    assert image_buffer_0.size == (341, 505)

    assert extracted_receipts[1].page_id == 0
    assert extracted_receipts[1].element_id == 1
    image_buffer_1 = Image.open(extracted_receipts[1].buffer)
    assert image_buffer_1.size == (461, 908)

    assert extracted_receipts[2].page_id == 0
    assert extracted_receipts[2].element_id == 2
    image_buffer_2 = Image.open(extracted_receipts[2].buffer)
    assert image_buffer_2.size == (471, 790)

    assert extracted_receipts[3].page_id == 0
    assert extracted_receipts[3].element_id == 3
    image_buffer_3 = Image.open(extracted_receipts[3].buffer)
    assert image_buffer_3.size == (464, 1200)

    assert extracted_receipts[4].page_id == 0
    assert extracted_receipts[4].element_id == 4
    image_buffer_4 = Image.open(extracted_receipts[4].buffer)
    assert image_buffer_4.size == (530, 943)

    assert extracted_receipts[5].page_id == 0
    assert extracted_receipts[5].element_id == 5
    image_buffer_5 = Image.open(extracted_receipts[5].buffer)
    assert image_buffer_5.size == (367, 593)


def test_multi_page_receipt_split(
    multi_receipts_multi_page_path, multi_receipts_multi_page_json_path
):
    input_sample = PathInput(multi_receipts_multi_page_path)
    with open(multi_receipts_multi_page_json_path, "rb") as f:
        response = json.load(f)
    doc = MultiReceiptsDetectorV1(response["document"]["inference"])
    extracted_receipts = extract_receipts(input_sample, doc)
    assert len(extracted_receipts) == 5

    assert extracted_receipts[0].page_id == 0
    assert extracted_receipts[0].element_id == 0
    image_buffer_0 = Image.open(extracted_receipts[0].buffer)
    assert image_buffer_0.size == (198, 566)

    assert extracted_receipts[1].page_id == 0
    assert extracted_receipts[1].element_id == 1
    image_buffer_1 = Image.open(extracted_receipts[1].buffer)
    assert image_buffer_1.size == (206, 382)

    assert extracted_receipts[2].page_id == 0
    assert extracted_receipts[2].element_id == 2
    image_buffer_2 = Image.open(extracted_receipts[2].buffer)
    assert image_buffer_2.size == (195, 231)

    assert extracted_receipts[3].page_id == 1
    assert extracted_receipts[3].element_id == 0
    image_buffer_3 = Image.open(extracted_receipts[3].buffer)
    assert image_buffer_3.size == (213, 356)

    assert extracted_receipts[4].page_id == 1
    assert extracted_receipts[4].element_id == 1
    image_buffer_4 = Image.open(extracted_receipts[4].buffer)
    assert image_buffer_4.size == (212, 516)
