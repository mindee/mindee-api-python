import pytest
from argparse import Namespace
from mindee.http import HTTPException
from mindee.__main__ import call_endpoint


@pytest.fixture
def custom_doc():
    return Namespace(
        product_name="custom",
        doc_type="license_plate",
        api_username="mindee",
        api_key="",
        raise_on_error=True,
        cut_pdf=True,
        input_type="path",
        path="./tests/data/license_plates/plate.png",
    )


@pytest.fixture
def invoice_doc():
    return Namespace(
        product_name="invoice",
        invoice_api_key="",
        raise_on_error=True,
        cut_pdf=True,
        input_type="path",
        path="./tests/data/invoices/invoice.pdf",
    )


def test_cli_custom_doc(custom_doc):
    with pytest.raises(HTTPException):
        call_endpoint(custom_doc)


def test_cli_invoice_doc(invoice_doc):
    with pytest.raises(HTTPException):
        call_endpoint(invoice_doc)
