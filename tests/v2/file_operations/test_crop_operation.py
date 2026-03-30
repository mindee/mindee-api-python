import json

import pytest
from PIL import Image

from mindee.v2.file_operations.crop import Crop
from mindee.input.sources.path_input import PathInput
from mindee.v2.product.crop.crop_response import (
    CropResponse,
)
from tests.utils import V2_PRODUCT_DATA_DIR


@pytest.fixture
def crops_single_page_path():
    return V2_PRODUCT_DATA_DIR / "crop" / "default_sample.jpg"


@pytest.fixture
def crops_multi_page_path():
    return V2_PRODUCT_DATA_DIR / "crop" / "multipage_sample.pdf"


@pytest.fixture
def crops_single_page_json_path():
    return V2_PRODUCT_DATA_DIR / "crop" / "crop_single.json"


@pytest.fixture
def crops_multi_page_json_path():
    return V2_PRODUCT_DATA_DIR / "crop" / "crop_multiple.json"


def test_single_page_crop_split(crops_single_page_path, crops_single_page_json_path):
    input_sample = PathInput(crops_single_page_path)
    with open(crops_single_page_json_path, "rb") as f:
        response = json.load(f)
    doc = CropResponse(response)
    extracted_crops = Crop.extract_crops(input_sample, doc.inference.result.crops)
    assert len(extracted_crops) == 1

    assert extracted_crops[0].page_id == 0
    assert extracted_crops[0].element_id == 0
    image_buffer_0 = Image.open(extracted_crops[0].buffer)
    assert image_buffer_0.size == (2823, 1571)


def test_multi_page_receipt_split(crops_multi_page_path, crops_multi_page_json_path):
    input_sample = PathInput(crops_multi_page_path)
    with open(crops_multi_page_json_path, "rb") as f:
        response = json.load(f)
    doc = CropResponse(response)
    extracted_crops = Crop.extract_crops(input_sample, doc.inference.result.crops)
    assert len(extracted_crops) == 2

    assert extracted_crops[0].page_id == 0
    assert extracted_crops[0].element_id == 0
    image_buffer_0 = Image.open(extracted_crops[0].buffer)
    assert image_buffer_0.size == (156, 758)

    assert extracted_crops[1].page_id == 0
    assert extracted_crops[1].element_id == 1
    image_buffer_1 = Image.open(extracted_crops[1].buffer)
    assert image_buffer_1.size == (187, 690)
