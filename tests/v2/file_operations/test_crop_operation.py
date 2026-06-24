from __future__ import annotations

import json

import pytest

from mindee.input.path_input import PathInput
from mindee.v2.product.crop.crop_response import (
    CropResponse,
)
from tests.utils import V2_PRODUCT_DATA_DIR

Image = pytest.importorskip("PIL.Image")


@pytest.mark.pillow
@pytest.mark.pypdfium2
def test_single_page_crop():
    input_sample = PathInput(V2_PRODUCT_DATA_DIR / "crop" / "default_sample.jpg")
    with open(V2_PRODUCT_DATA_DIR / "crop" / "default_sample.json", "rb") as f:
        response = CropResponse(json.load(f))
    extracted_crops = response.inference.result.extract_from_input_source(input_sample)
    assert len(extracted_crops) == 2

    crop0 = extracted_crops[0]
    assert crop0.page_id == 0
    assert crop0.element_id == 0
    assert crop0.filename == "default_sample_page-001-item-001.jpg"
    assert Image.open(crop0.buffer).size == (1057, 2071)

    crop1 = extracted_crops[1]
    assert crop1.page_id == 0
    assert crop1.element_id == 1
    assert crop1.filename == "default_sample_page-001-item-002.jpg"
    assert Image.open(crop1.buffer).size == (1298, 1869)


@pytest.mark.pillow
@pytest.mark.pypdfium2
def test_multi_page_crop():
    input_sample = PathInput(V2_PRODUCT_DATA_DIR / "crop" / "multipage_sample.pdf")
    with open(V2_PRODUCT_DATA_DIR / "crop" / "multipage_sample.json", "rb") as f:
        response = CropResponse(json.load(f))
    extracted_crops = response.inference.result.extract_from_input_source(input_sample)
    assert len(extracted_crops) == 5

    crop0 = extracted_crops[0]
    assert crop0.page_id == 0
    assert crop0.element_id == 0
    assert crop0.filename == "multipage_sample_page-001-item-001.jpg"
    assert Image.open(crop0.buffer).size == (200, 553)

    crop1 = extracted_crops[1]
    assert crop1.page_id == 0
    assert crop1.element_id == 1
    assert crop1.filename == "multipage_sample_page-001-item-002.jpg"
    assert Image.open(crop1.buffer).size == (203, 333)

    crop4 = extracted_crops[4]
    assert crop4.page_id == 1
    assert crop4.element_id == 1
    assert crop4.filename == "multipage_sample_page-002-item-002.jpg"
    assert Image.open(crop4.buffer).size == (197, 520)
