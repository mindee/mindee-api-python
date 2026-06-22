from pathlib import Path

import pytest

from mindee.input.path_input import PathInput
from mindee.v1.client import Client
from mindee.v1.parsing.common import Document
from mindee.v1.pdf.pdf_extractor import PDFExtractor
from mindee.v1.product.invoice.invoice_v4 import InvoiceV4
from mindee.v1.product.invoice_splitter.invoice_splitter_v1 import InvoiceSplitterV1
from tests.utils import V1_PRODUCT_DATA_DIR, levenshtein_ratio
from tests.v1.product import get_id, get_version


@pytest.fixture
def invoice_splitter_5p_path():
    return V1_PRODUCT_DATA_DIR / "invoice_splitter" / "invoice_5p.pdf"


def prepare_invoice_return(rst_file_path: Path, invoice_prediction: Document):
    with open(rst_file_path) as rst_file:
        rst_content = rst_file.read()
    parsing_version = invoice_prediction.inference.product.version
    parsing_id = invoice_prediction.id
    rst_content = rst_content.replace(get_version(rst_content), parsing_version)
    rst_content = rst_content.replace(get_id(rst_content), parsing_id)
    return rst_content


@pytest.mark.pillow
@pytest.mark.pypdfium2
@pytest.mark.integration
def test_pdf_should_extract_invoices_strict():
    client = Client()
    invoice_splitter_input = PathInput(
        V1_PRODUCT_DATA_DIR / "invoice_splitter" / "default_sample.pdf"
    )
    response = client.enqueue_and_parse(
        InvoiceSplitterV1, invoice_splitter_input, close_file=False
    )
    inference = response.document.inference
    pdf_extractor = PDFExtractor(invoice_splitter_input)
    assert pdf_extractor.get_page_count() == 2

    extracted_pdfs_not_strict = pdf_extractor.extract_invoices(
        inference.prediction.invoice_page_groups
    )
    extracted_pdfs_strict = pdf_extractor.extract_invoices(
        inference.prediction.invoice_page_groups
    )
    extracted_base_pdfs = pdf_extractor.extract_documents(
        [int_list.page_indexes for int_list in inference.prediction.invoice_page_groups]
    )
    for i, extracted_pdf in enumerate(extracted_base_pdfs):
        assert extracted_pdf.filename == extracted_pdfs_strict[i].filename
        assert extracted_pdf.buffer.read() == extracted_pdfs_strict[i].buffer.read()

    assert len(extracted_pdfs_not_strict) == 2
    assert extracted_pdfs_not_strict[0].filename == "default_sample_001-001.pdf"
    assert extracted_pdfs_not_strict[1].filename == "default_sample_002-002.pdf"

    invoice_0 = client.parse(InvoiceV4, extracted_pdfs_not_strict[0].as_input_source())
    test_string_rst_invoice_0 = prepare_invoice_return(
        V1_PRODUCT_DATA_DIR
        / "invoices"
        / "response_v4"
        / "summary_full_invoice_p1.rst",
        invoice_0.document,
    )
    assert levenshtein_ratio(test_string_rst_invoice_0, str(invoice_0.document)) >= 0.97
