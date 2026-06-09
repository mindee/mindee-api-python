import os
from pathlib import Path

import pytest

from mindee.input.url_input_source import URLInputSource
from mindee.v1.client import Client
from mindee.v1.product.invoice import InvoiceV4
from tests.utils import cleanup_output_files


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def output_file_path():
    return Path("tests/data/output/")


@pytest.fixture
def reference_file_path():
    ref_path = os.getenv("MINDEE_V2_SE_TESTS_BLANK_PDF_URL")
    if ref_path is None:
        raise ValueError("MINDEE_V2_SE_TESTS_BLANK_PDF_URL not set")
    return ref_path


@pytest.mark.integration
def test_load_local_file(client, reference_file_path):
    url_source = URLInputSource(reference_file_path)
    local_source = url_source.as_local_input_source()
    result = client.parse(InvoiceV4, local_source)
    assert result.document.n_pages == 1
    assert result.document.filename == "blank_1.pdf"


@pytest.mark.integration
def test_custom_file_name(client, reference_file_path):
    url_source = URLInputSource(reference_file_path)
    local_source = url_source.as_local_input_source("customName.pdf")
    result = client.parse(InvoiceV4, local_source)
    assert result.document.n_pages == 1
    assert result.document.filename == "customName.pdf"


@pytest.mark.integration
def test_save_file(client, reference_file_path, output_file_path):
    url_source = URLInputSource(reference_file_path)
    url_source.save_to_file(output_file_path)
    assert os.path.exists(os.path.join(output_file_path, "blank_1.pdf"))


@pytest.mark.integration
def test_save_file_with_filename(client, reference_file_path, output_file_path):
    url_source = URLInputSource(reference_file_path)
    url_source.save_to_file(output_file_path, "customFileName.pdf")
    assert os.path.exists(os.path.join(output_file_path, "customFileName.pdf"))


@pytest.fixture(autouse=True)
def cleanup():
    yield
    cleanup_output_files(["blank_1.pdf", "customFileName.pdf"])
