import pytest
from argparse import Namespace

from tests.utils import clear_envvars

from mindee.__main__ import call_endpoint


@pytest.fixture
def custom_doc(monkeypatch):
    clear_envvars(monkeypatch)

    return Namespace(
        product_name="custom",
        doc_type="license_plate",
        username="mindee",
        api_key="",
        raise_on_error=True,
        cut_pdf=True,
        input_type="path",
        output_type="summary",
        path="./tests/data/license_plates/plate.png",
    )


@pytest.fixture
def invoice_doc(monkeypatch):
    clear_envvars(monkeypatch)

    return Namespace(
        product_name="invoice",
        invoice_api_key="",
        raise_on_error=True,
        cut_pdf=True,
        input_type="path",
        output_type="summary",
        path="./tests/data/invoices/invoice.pdf",
    )


def test_cli_custom_doc(custom_doc):
    with pytest.raises(RuntimeError):
        call_endpoint(custom_doc)


def test_cli_invoice_doc(invoice_doc):
    with pytest.raises(RuntimeError):
        call_endpoint(invoice_doc)
