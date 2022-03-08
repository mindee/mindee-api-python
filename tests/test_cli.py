import pytest
from argparse import Namespace

from tests.utils import clear_envvars

from mindee.__main__ import call_endpoint
from mindee.http import HTTPException


@pytest.fixture
def custom_doc(monkeypatch):
    clear_envvars(monkeypatch)
    return Namespace(
        product_name="custom",
        doc_type="license_plate",
        username="mindee",
        api_key="dummy",
        raise_on_error=True,
        cut_pdf=True,
        input_type="path",
        output_type="summary",
        include_words=False,
        path="./tests/data/license_plates/plate.png",
    )


@pytest.fixture
def ots_doc(monkeypatch):
    clear_envvars(monkeypatch)
    return Namespace(
        raise_on_error=True,
        cut_pdf=True,
        input_type="path",
        output_type="summary",
        include_words=False,
        path="./tests/data/invoices/invoice.pdf",
    )


def test_cli_custom_doc(custom_doc):
    with pytest.raises(HTTPException):
        call_endpoint(custom_doc)


def test_cli_invoice(ots_doc):
    ots_doc.product_name = "invoice"
    ots_doc.invoice_api_key = ""
    with pytest.raises(RuntimeError):
        call_endpoint(ots_doc)
    ots_doc.invoice_api_key = "dummy"
    with pytest.raises(HTTPException):
        call_endpoint(ots_doc)


def test_cli_receipt(ots_doc):
    ots_doc.product_name = "receipt"
    ots_doc.receipt_api_key = ""
    with pytest.raises(RuntimeError):
        call_endpoint(ots_doc)
    ots_doc.receipt_api_key = "dummy"
    with pytest.raises(HTTPException):
        call_endpoint(ots_doc)


def test_cli_financial_doc(ots_doc):
    ots_doc.product_name = "financial"
    ots_doc.invoice_api_key = ""
    ots_doc.receipt_api_key = ""
    with pytest.raises(RuntimeError):
        call_endpoint(ots_doc)
    ots_doc.invoice_api_key = "dummy"
    ots_doc.receipt_api_key = "dummy"
    with pytest.raises(HTTPException):
        call_endpoint(ots_doc)


def test_cli_passport(ots_doc):
    ots_doc.product_name = "passport"
    ots_doc.passport_api_key = ""
    with pytest.raises(RuntimeError):
        call_endpoint(ots_doc)
    ots_doc.passport_api_key = "dummy"
    with pytest.raises(HTTPException):
        call_endpoint(ots_doc)
