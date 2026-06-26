from os import getenv

import pytest

from mindee import (
    ExtractionParameters,
    ExtractionResponse,
    SplitParameters,
    SplitResponse,
)
from mindee.input.path_input import PathInput
from mindee.v2.client import Client
from tests.utils import OUTPUT_DIR, V2_PRODUCT_DATA_DIR, cleanup_output_files


def check_findoc_return(findoc_response: ExtractionResponse):
    assert len(findoc_response.inference.model.id) > 0
    assert findoc_response.inference.result.fields.get("total_amount").value > 0


output_files = [
    "default_sample_pages-001-001.pdf",
    "default_sample_pages-002-002.pdf",
]


@pytest.mark.pypdfium2
@pytest.mark.integration
def test_pdf_should_extract_splits():

    client = Client()
    split_input = PathInput(V2_PRODUCT_DATA_DIR / "split" / "default_sample.pdf")
    response = client.enqueue_and_get_result(
        SplitResponse,
        split_input,
        SplitParameters(
            getenv("MINDEE_V2_SE_TESTS_SPLIT_MODEL_ID"),
            close_file=False,
        ),
    )
    assert response.inference.file.page_count == 2

    extracted_splits = response.inference.result.extract_from_input_source(split_input)

    assert len(extracted_splits) == 2
    assert extracted_splits[0].filename == output_files[0]
    assert extracted_splits[1].filename == output_files[1]

    invoice_0 = client.enqueue_and_get_result(
        ExtractionResponse,
        extracted_splits[0].as_input_source(),
        ExtractionParameters(
            getenv("MINDEE_V2_SE_TESTS_FINDOC_MODEL_ID"), close_file=False
        ),
    )
    check_findoc_return(invoice_0)
    extracted_splits.save_all_to_disk(OUTPUT_DIR)
    for i in range(len(extracted_splits)):
        local_input = PathInput(OUTPUT_DIR / output_files[i])
        try:
            assert local_input.page_count == extracted_splits[i].page_count
        finally:
            local_input.close()
    split_input.close()


@pytest.fixture(scope="module", autouse=True)
def cleanup():
    yield
    cleanup_output_files(output_files)
