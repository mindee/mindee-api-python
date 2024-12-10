import os
from pathlib import Path

import pytest

from mindee import Client
from mindee.product.invoice import InvoiceV4


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def output_file_path():
    return Path("tests/data/output/")


@pytest.fixture
def reference_file_path():
    return "https://github.com/mindee/client-lib-test-data/blob/main/products/invoice_splitter/invoice_5p.pdf?raw=true"


@pytest.mark.integration
def test_load_local_file(client, reference_file_path):
    url_source = client.source_from_url(reference_file_path)
    local_source = url_source.as_local_input_source()
    result = client.parse(InvoiceV4, local_source)
    assert result.document.n_pages == 5
    assert result.document.filename == "invoice_5p.pdf"


@pytest.mark.integration
def test_custom_file_name(client, reference_file_path):
    url_source = client.source_from_url(reference_file_path)
    local_source = url_source.as_local_input_source("customName.pdf")
    result = client.parse(InvoiceV4, local_source)
    assert result.document.n_pages == 5
    assert result.document.filename == "customName.pdf"


@pytest.mark.integration
def test_save_file(client, reference_file_path, output_file_path):
    url_source = client.source_from_url(reference_file_path)
    url_source.save_to_file(output_file_path)
    assert os.path.exists(os.path.join(output_file_path, "invoice_5p.pdf"))


@pytest.mark.integration
def test_save_file_with_filename(client, reference_file_path, output_file_path):
    url_source = client.source_from_url(reference_file_path)
    url_source.save_to_file(output_file_path, "customFileName.pdf")
    assert os.path.exists(os.path.join(output_file_path, "customFileName.pdf"))


@pytest.fixture(autouse=True)
def cleanup(request, output_file_path: Path):
    def remove_test_files():
        generated_files = [
            Path.resolve(output_file_path / "invoice_5p.pdf"),
            Path.resolve(output_file_path / "customFileName.pdf"),
        ]
        for filepath in generated_files:
            if os.path.exists(filepath):
                os.remove(filepath)

    request.addfinalizer(remove_test_files)
