import json

import pytest
from PIL import Image

from mindee.image_extraction.common import extract_multiple_images_from_source
from mindee.input import PathInput
from mindee.product import BarcodeReaderV1
from tests.test_inputs import PRODUCT_DATA_DIR


@pytest.fixture
def barcode_path():
    return PRODUCT_DATA_DIR / "barcode_reader" / "default_sample.jpg"


@pytest.fixture
def barcode_json_path():
    return PRODUCT_DATA_DIR / "barcode_reader" / "response_v1" / "complete.json"


def test_barcode_image_extraction(barcode_path, barcode_json_path):
    with open(barcode_json_path, "rb") as f:
        response = json.load(f)
    inference = BarcodeReaderV1(response["document"]["inference"])
    barcodes_1 = [code_1d.polygon for code_1d in inference.prediction.codes_1d]
    barcodes_2 = [code_2d.polygon for code_2d in inference.prediction.codes_2d]
    input_source = PathInput(barcode_path)
    extracted_barcodes_1d = extract_multiple_images_from_source(
        input_source, 0, barcodes_1
    )
    extracted_barcodes_2d = extract_multiple_images_from_source(
        input_source, 0, barcodes_2
    )
    assert len(extracted_barcodes_1d) == 1
    assert len(extracted_barcodes_2d) == 2

    assert Image.open(extracted_barcodes_1d[0].buffer).size == (353, 200)
    assert Image.open(extracted_barcodes_2d[0].buffer).size == (214, 216)
    assert Image.open(extracted_barcodes_2d[1].buffer).size == (193, 201)
