import pytest

from mindee import Client
from mindee.extraction.pdf_extractor.pdf_extractor import PdfExtractor
from mindee.input.local_response import LocalResponse
from mindee.input.sources.path_input import PathInput
from mindee.product.invoice_splitter.invoice_splitter_v1 import InvoiceSplitterV1
from mindee.product.invoice_splitter.invoice_splitter_v1_document import (
    InvoiceSplitterV1Document,
)
from tests.test_inputs import PRODUCT_DATA_DIR


@pytest.fixture
def invoice_default_sample_path():
    return PRODUCT_DATA_DIR / "invoices" / "default_sample.jpg"


@pytest.fixture
def invoice_splitter_5p_path():
    return PRODUCT_DATA_DIR / "invoice_splitter" / "invoice_5p.pdf"


@pytest.fixture
def loaded_prediction():
    dummy_client = Client("dummy_key")
    loaded_prediction_path = (
        PRODUCT_DATA_DIR / "invoice_splitter" / "response_v1" / "complete.json"
    )
    input_response = LocalResponse(loaded_prediction_path)
    response = dummy_client.load_prediction(InvoiceSplitterV1, input_response)
    prediction: InvoiceSplitterV1Document = response.document.inference.prediction
    return prediction


def test_image_should_extract_pdf(invoice_default_sample_path):
    jpg_input = PathInput(invoice_default_sample_path)
    assert not jpg_input.is_pdf()
    extractor = PdfExtractor(jpg_input)
    assert extractor.get_page_count() == 1


def test_pdf_should_extract_invoices_no_strict(
    invoice_splitter_5p_path, loaded_prediction
):
    pdf_input = PathInput(invoice_splitter_5p_path)
    extractor = PdfExtractor(pdf_input)
    assert extractor.get_page_count() == 5
    extracted_pdfs_no_strict = extractor.extract_invoices(
        loaded_prediction.invoice_page_groups
    )

    assert len(extracted_pdfs_no_strict) == 3
    assert extracted_pdfs_no_strict[0].get_page_count() == 1
    assert extracted_pdfs_no_strict[0].filename == "invoice_5p_001-001.pdf"

    assert extracted_pdfs_no_strict[1].get_page_count() == 3
    assert extracted_pdfs_no_strict[1].filename == "invoice_5p_002-004.pdf"

    assert extracted_pdfs_no_strict[2].get_page_count() == 1
    assert extracted_pdfs_no_strict[2].filename == "invoice_5p_005-005.pdf"


def test_pdf_should_extract_invoices_strict(
    invoice_splitter_5p_path, loaded_prediction
):
    pdf_input = PathInput(invoice_splitter_5p_path)
    extractor = PdfExtractor(pdf_input)
    assert extractor.get_page_count() == 5
    extracted_pdfs_strict = extractor.extract_invoices(
        loaded_prediction.invoice_page_groups, True
    )

    assert len(extracted_pdfs_strict) == 2
    assert extracted_pdfs_strict[0].get_page_count() == 1
    assert extracted_pdfs_strict[0].filename == "invoice_5p_001-001.pdf"

    assert extracted_pdfs_strict[1].get_page_count() == 4
    assert extracted_pdfs_strict[1].filename == "invoice_5p_002-005.pdf"
