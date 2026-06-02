import os
from os import getenv

import pytest

from mindee import (
    ExtractionParameters,
    ExtractionResponse,
    CropParameters,
    CropResponse,
)
from mindee.v2.client import Client
from mindee.input.path_input import PathInput
from mindee.v2.file_operations.crop import extract_crops
from tests.utils import OUTPUT_DIR, V2_PRODUCT_DATA_DIR, cleanup_output_files


@pytest.fixture
def crop_sample():
    return V2_PRODUCT_DATA_DIR / "crop" / "default_sample.jpg"


def check_findoc_return(findoc_response: ExtractionResponse):
    assert len(findoc_response.inference.model.id) > 0
    assert findoc_response.inference.result.fields.get("total_amount").value > 0


@pytest.mark.integration
def test_image_should_extract_crops():
    client = Client()
    crop_input = PathInput(V2_PRODUCT_DATA_DIR / "crop" / "default_sample.jpg")
    response = client.enqueue_and_get_result(
        CropResponse,
        crop_input,
        CropParameters(getenv("MINDEE_V2_SE_TESTS_CROP_MODEL_ID"), close_file=False),
    )
    assert len(response.inference.result.crops) == 2

    extracted_images = extract_crops(crop_input, response.inference.result.crops)

    assert len(extracted_images) == 2
    assert extracted_images[0].filename == "default_sample.jpg_page1-0.jpg"
    assert extracted_images[1].filename == "default_sample.jpg_page1-1.jpg"

    invoice_0 = client.enqueue_and_get_result(
        ExtractionResponse,
        extracted_images[0].as_input_source(),
        ExtractionParameters(
            getenv("MINDEE_V2_SE_TESTS_FINDOC_MODEL_ID"), close_file=False
        ),
    )
    check_findoc_return(invoice_0)
    extracted_images.save_all_to_disk(OUTPUT_DIR)
    # note: flaky
    assert os.path.getsize(OUTPUT_DIR / "crop_001.jpg") in (187601, 199685)
    assert os.path.getsize(OUTPUT_DIR / "crop_002.jpg") in (197978, 199433)


@pytest.fixture(scope="module", autouse=True)
def cleanup():
    yield
    cleanup_output_files(["crop_001.jpg", "crop_002.jpg"])
