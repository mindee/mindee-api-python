import os
from os import getenv

import pytest

from mindee import (
    CropParameters,
    CropResponse,
    ExtractionParameters,
    ExtractionResponse,
)
from mindee.input.path_input import PathInput
from mindee.v2.client import Client
from mindee.v2.file_operations.crop import extract_multiple_crops
from tests.utils import OUTPUT_DIR, V2_PRODUCT_DATA_DIR, cleanup_output_files


def check_findoc_return(findoc_response: ExtractionResponse):
    assert len(findoc_response.inference.model.id) > 0
    assert findoc_response.inference.result.fields.get("total_amount").value > 0


output_files = [
    "default_sample_page-001-item-001.jpg",
    "default_sample_page-001-item-002.jpg",
]


@pytest.mark.pillow
@pytest.mark.pypdfium2
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

    extracted_crops = extract_multiple_crops(
        crop_input, response.inference.result.crops
    )

    assert len(extracted_crops) == 2
    assert extracted_crops[0].filename == output_files[0]
    assert extracted_crops[1].filename == output_files[1]

    invoice_0 = client.enqueue_and_get_result(
        ExtractionResponse,
        extracted_crops[0].as_input_source(),
        ExtractionParameters(
            getenv("MINDEE_V2_SE_TESTS_FINDOC_MODEL_ID"), close_file=False
        ),
    )
    check_findoc_return(invoice_0)
    extracted_crops.save_all_to_disk(OUTPUT_DIR)
    crop0_size = os.path.getsize(OUTPUT_DIR / output_files[0])
    crop1_size = os.path.getsize(OUTPUT_DIR / output_files[1])
    assert 180000 <= crop0_size <= 199685
    assert 190000 <= crop1_size <= 199433


@pytest.fixture(scope="module", autouse=True)
def cleanup():
    yield
    cleanup_output_files(output_files)
