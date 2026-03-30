import os
from os import getenv

import pytest

from mindee import (
    ClientV2,
    InferenceParameters,
    InferenceResponse,
    CropParameters,
    CropResponse,
)
from mindee.input.sources.path_input import PathInput
from mindee.v2 import Crop
from tests.utils import OUTPUT_DIR, V2_PRODUCT_DATA_DIR, cleanup_output_files


@pytest.fixture
def crop_sample():
    return V2_PRODUCT_DATA_DIR / "crop" / "default_sample.jpg"


def check_findoc_return(findoc_response: InferenceResponse):
    assert len(findoc_response.inference.model.id) > 0
    assert findoc_response.inference.result.fields.get("total_amount").value > 0


@pytest.mark.integration
def test_image_should_extract_crops():
    client = ClientV2()
    crop_input = PathInput(V2_PRODUCT_DATA_DIR / "crop" / "default_sample.jpg")
    response = client.enqueue_and_get_result(
        CropResponse,
        crop_input,
        CropParameters(getenv("MINDEE_V2_SE_TESTS_CROP_MODEL_ID"), close_file=False),
    )
    assert len(response.inference.result.crops) == 2

    extracted_images = Crop.extract_crops(crop_input, response.inference.result.crops)

    assert len(extracted_images) == 2
    assert extracted_images[0].filename == "default_sample.jpg_page1-0.jpg"
    assert extracted_images[1].filename == "default_sample.jpg_page1-1.jpg"

    invoice_0 = client.enqueue_and_get_result(
        InferenceResponse,
        extracted_images[0].as_input_source(),
        InferenceParameters(
            getenv("MINDEE_V2_SE_TESTS_FINDOC_MODEL_ID"), close_file=False
        ),
    )
    check_findoc_return(invoice_0)
    for i, extracted_image in enumerate(extracted_images):
        extracted_image.save_to_file(OUTPUT_DIR / f"crop_{i + 1:03d}.jpg")
    assert os.path.getsize(OUTPUT_DIR / "crop_001.jpg") == 198887
    assert os.path.getsize(OUTPUT_DIR / "crop_002.jpg") == 197443


@pytest.fixture(scope="module", autouse=True)
def cleanup():
    yield
    cleanup_output_files(["crop_001.jpg", "crop_002.jpg"])
