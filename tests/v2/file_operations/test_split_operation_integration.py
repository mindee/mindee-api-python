from os import getenv

import pytest

from mindee import (
    ClientV2,
    InferenceParameters,
    InferenceResponse,
    SplitParameters,
    SplitResponse,
)
from mindee.input.sources.path_input import PathInput
from mindee.v2 import Split
from tests.utils import OUTPUT_DIR, V2_PRODUCT_DATA_DIR, cleanup_output_files


@pytest.fixture
def invoice_splitter_5p_path():
    return V2_PRODUCT_DATA_DIR / "split" / "invoice_5p.pdf"


def check_findoc_return(findoc_response: InferenceResponse):
    assert len(findoc_response.inference.model.id) > 0
    assert findoc_response.inference.result.fields.get("total_amount").value > 0


@pytest.mark.integration
def test_pdf_should_extract_splits():
    client = ClientV2()
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

    extracted_pdfs = Split.extract_splits(split_input, response.inference.result.splits)

    assert len(extracted_pdfs) == 2
    assert extracted_pdfs[0].filename == "default_sample_001-001.pdf"
    assert extracted_pdfs[1].filename == "default_sample_002-002.pdf"

    invoice_0 = client.enqueue_and_get_result(
        InferenceResponse,
        extracted_pdfs[0].as_input_source(),
        InferenceParameters(
            getenv("MINDEE_V2_SE_TESTS_FINDOC_MODEL_ID"), close_file=False
        ),
    )
    check_findoc_return(invoice_0)
    for i, extracted_pdf in enumerate(extracted_pdfs):
        extracted_pdf.save_to_file(OUTPUT_DIR / f"split_{i + 1:03d}.pdf")
    for i in range(len(extracted_pdfs)):
        local_input = PathInput(OUTPUT_DIR / f"split_{i + 1:03d}.pdf")
        try:
            assert local_input.page_count == extracted_pdfs[i].get_page_count()
        finally:
            local_input.close()
    split_input.close()


@pytest.fixture(scope="module", autouse=True)
def cleanup():
    yield
    cleanup_output_files(["split_001.pdf", "split_002.pdf"])
